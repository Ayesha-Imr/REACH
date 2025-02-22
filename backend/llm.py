from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import List
import json
from pydantic import ValidationError
from langchain_ibm import ChatWatsonx
from langchain.schema import SystemMessage, HumanMessage
from langchain_ibm import ChatWatsonx
from langchain.tools import tool
from backend.database import query_db
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
import streamlit as st


# load_dotenv()

# os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
# watson_api_key = os.environ["IBM_WATSON_KEY"]
# url = "https://us-south.ml.cloud.ibm.com"  
# watson_project_id = os.environ["IBM_PROJECT_ID"] 


tavily_api_key = st.secrets["tavily"]["TAVILY_API_KEY"]
watson_api_key = st.secrets["ibm"]["IBM_WATSON_KEY"]
url = "https://us-south.ml.cloud.ibm.com"  
watson_project_id = st.secrets["ibm"]["IBM_PROJECT_ID"] 


# Function to get the summary of the startup given the extracted information from uploaded data sources
def get_summary(info):

    system_prompt = """You are an expert analyst skilled in evaluating startups based on their website content, documents, and pitch decks.
    Given the extracted textual content of a startup’s materials, analyze and generate a concise, fact-based summary (max 300 words) using only
    the information explicitly present in the input. Do not infer, assume, or generate any details that are not explicitly stated.

    Your summary should include the following key points only if they are present in the input text:

    - Startup Overview – What the startup does, its core product/service, and industry.
    - Problem & Solution – What problem it solves and how it provides value.
    - Target Audience & Market – Who the product is for and the market potential.
    - Business Model – How it makes money (if stated).
    - Stage & Traction – What stage it is in (idea, MVP, early revenue, growth, etc.), notable milestones, funding (if mentioned), and key partnerships.
    - Competitive Advantage – Any unique features, technology, or differentiators.

    Ensure the summary is clear, structured, and objective, strictly reflecting the provided information.
    If any of the above details are missing from the input, omit them rather than speculating or fabricating information.
    Keep it concise, factual, and insightful."""


    # Define model parameters
    chat_model = ChatWatsonx(
        model_id="ibm/granite-3-8b-instruct",
        url=url,
        apikey=watson_api_key,
        project_id=watson_project_id,
        params={
            "decoding_method": "greedy",
            "temperature": 0,
            "min_new_tokens": 200,
            "max_new_tokens": 500,
        },
    )

    # Create message objects
    system_message = SystemMessage(content=system_prompt)
    user_message = HumanMessage(content=info)

    # Generate response
    response = chat_model([system_message, user_message])

    # Output the generated summary
    print(response.content)
    return response.content


# Function to get the keywords for Reddit, Twitter, and Instagram based on the startup information
def get_keywords(info):

    class RedditQueries(BaseModel):
        subreddits: List[str] = Field(..., description="List of three subreddits for optimized Reddit searches.")
        queries: List[str] = Field(..., description="List of three optimized search queries for Reddit.")

    class SocialMediaQueries(BaseModel):
        reddit: RedditQueries = Field(..., description="Dictionary containing subreddits and queries for Reddit.")
        twitter: List[str] = Field(..., description="List of three optimized search queries for Twitter/X.")
        instagram: List[str] = Field(..., description="List of three optimized search hashtags for Instagram.")


    system_prompt = """You are a startup research assistant specializing in market research for early-stage startups. 
        Your task is to analyze the provided information about a startup—including its industry, target audience, value proposition, 
        and competitors—and generate the following:
        - 3 optimized search queries for Reddit along with the corresponding subreddit to search from. Each search query should be no longer than 3 words.
        - 3 optimized search queries for Twitter/X. Each search query should be no longer than 3 words.
        - 3 optimized search hashtags for Instagram.

        These queries should help the startup gather:

        - Trending Topics & Discussions – What conversations, pain points, or emerging trends are relevant to the startup’s field?
        - Potential Customer Insights – What do potential users or customers discuss, ask, or complain about in this space?
        - Competitor & Industry Analysis – Who are similar startups or competitors, and what engagement strategies work for them?

        Guidelines for Generating Queries:
        
        - Reddit: Focus on finding discussions in relevant subreddits, common questions, challenges, or product recommendations. 
        Use natural language phrasing that people might post.
        - Instagram: Target hashtags, influencers, and content themes that highlight what’s popular in the startup's niche.
        - Twitter/X: Look for real-time trends, viral tweets, and industry news using keywords and phrases.

        Give your answer in JSON format with the following fields (where subreddit1 corresponds to query1 for Reddit, and so on): 
        {'reddit': {'subreddits': ['subreddit1', 'subreddit2', 'subreddit2'], 'queries': ['query1', 'query2', 'query3']}, 'twitter': ['query1', 'query2', 'query3'], 'instagram': ['hashtag1', 'hashtag2', 'hashtag3']}"""


    # Define model parameters
    chat_model = ChatWatsonx(
        model_id="ibm/granite-3-8b-instruct",
        url=url,
        apikey=watson_api_key,
        project_id=watson_project_id,
        params={
            "decoding_method": "greedy",
            "temperature": 0,
            "min_new_tokens": 200,
            "max_new_tokens": 500,
        },
    )

    # Create message objects
    system_message = SystemMessage(content=system_prompt)
    user_message = HumanMessage(content=info)

    # Generate response
    response = chat_model([system_message, user_message])

    # Parse the JSON response
    try:
        response_data = json.loads(response.content)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

    # Validate the parsed data using Pydantic
    try:
        validated_data = SocialMediaQueries(**response_data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

    # Output the validated data
    print(validated_data.model_dump_json())
    return validated_data

# Function to get insights from Instagram data
def get_instagram_insights(startup_info, instagram_data):

    class InstagramInsights(BaseModel):
        platform: str = Field("Instagram", description="Social media platform name")
        content_trends: str = Field(..., description="Trends related to content, aesthetics, and themes")
        audience_behavior: str = Field(..., description="How users interact, what they discuss, and their preferences")
        influencer_landscape: str = Field(..., description="Notable influencers, brands, and creators in the space")
        content_strategy: str = Field(..., description="How the startup should create engaging and valuable content")
        engagement_tactics: str = Field(..., description="Strategies to increase engagement and follower growth on Instagram")


    system_prompt = """You are a market intelligence and social media strategist specializing in Instagram. 
        Your task is to analyze the startup’s description and the extracted Instagram captions to uncover **key trends, audience preferences, and content strategies.** 
        You will also provide recommendations on how the startup can **build a strong presence, attract followers, and increase engagement** on Instagram.

        ### Key Insights to Generate:
        1. **Visual & Content Trends** – What themes, aesthetics, and storytelling styles are most popular in this industry? What types of posts (e.g., reels, carousels, behind-the-scenes content) get the highest engagement?
        2. **Audience Interests & Behavior** – What topics are resonating with Instagram users in this niche? What questions, desires, or trends keep appearing in the discussions?
        3. **Influencer & Brand Landscape** – Who are the key influencers, brands, or creators driving engagement in this space? What strategies do they use to connect with their audience?
        4. **Content & Brand Strategy** – What kind of posts should the startup create to **stand out and provide value?** How can it craft visually appealing, shareable, and engaging content?
        5. **Engagement & Growth Strategies** – What Instagram-specific tactics (e.g., collaborations, hashtag strategies, viral challenges, interactive stories) should the startup leverage to **attract and retain followers?** 

        Important Note: If the provided Instagram data does not contain any significant or relevant info about one or more of the above points,
        you can generate hypothetical insights based on the startup description and general Instagram trends in the industry, as well as your own valid knowledge. 

        Output Format (JSON):
        {
        "platform": "Instagram",
        "content_trends": "...",
        "audience_behavior": "...",
        "influencer_landscape": "...",
        "content_strategy": "...",
        "engagement_tactics": "..."
        }"""


    # Define model parameters
    chat_model = ChatWatsonx(
        model_id="ibm/granite-3-8b-instruct",
        url=url,
        apikey=watson_api_key,
        project_id=watson_project_id,
        params={
            "decoding_method": "greedy",
            "temperature": 0,
            "min_new_tokens": 500,
            "max_new_tokens": 1000,
        },
    )

    # Create message objects
    system_message = SystemMessage(content=system_prompt)
    user_prompt = f"Startup Info: {startup_info}\nInstagram Data: {instagram_data}"
    user_message = HumanMessage(content=user_prompt)

    # Generate response
    response = chat_model([system_message, user_message])

    # Parse the JSON response
    try:
        response_data = json.loads(response.content)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

    # Validate the parsed data using Pydantic
    try:
        validated_data = InstagramInsights(**response_data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

    # Output the validated data
    print(validated_data.model_dump_json())
    return validated_data

# Function to get insights from Reddit data
def get_reddit_insights(startup_info, instagram_data):

    class RedditInsights(BaseModel):
        platform: str = Field("Reddit", description="Social media platform name")
        market_trends: str = Field(..., description="Industry trends and emerging discussions in subreddits")
        customer_insights: str = Field(..., description="Pain points, knowledge gaps, and unmet customer needs")
        competitive_landscape: str = Field(..., description="Competitors, brands, and their engagement strategies")
        content_strategy: str = Field(..., description="Best-performing content types for engagement on Reddit")
        community_engagement: str = Field(..., description="How the startup should participate and build authority in relevant subreddits")


    system_prompt = """You are a market intelligence and audience research expert specializing in Reddit. 
        Your task is to analyze the startup’s description and the extracted Reddit discussions to uncover **deep insights into industry trends, customer pain points, and competitor strategies.** 
        You will also provide recommendations on how the startup can **engage effectively within relevant subreddits** to build brand awareness, attract potential customers, and position itself as an authority in the space.

        ### Key Insights to Generate:
        1. **Industry & Market Trends** – What major trends, innovations, or concerns are dominating discussions in relevant subreddits? What new developments are shaping customer preferences and behaviors?
        2. **Customer Pain Points & Unmet Needs** – What problems, frustrations, or knowledge gaps are Reddit users frequently discussing? What are they looking for in solutions?
        3. **Competitor & Community Insights** – What competing products, brands, or services are being discussed? How do users feel about them? What strategies or responses are working for competitors?
        4. **Content & Engagement Strategy** – What types of Reddit posts (e.g., AMA sessions, case studies, deep-dive analysis, meme marketing, expert insights) receive the highest engagement? How can the startup craft engaging content?
        5. **Community Participation & Growth Strategies** – How can the startup **organically** integrate into these Reddit communities, contribute value, and drive engagement **without coming across as promotional**?

        Output Format (JSON):
        {
        "platform": "Reddit",
        "market_trends": "...",
        "customer_insights": "...",
        "competitive_landscape": "...",
        "content_strategy": "...",
        "community_engagement": "..."
        }"""


    # Define model parameters
    chat_model = ChatWatsonx(
        model_id="ibm/granite-3-8b-instruct",
        url=url,
        apikey=watson_api_key,
        project_id=watson_project_id,
        params={
            "decoding_method": "greedy",
            "temperature": 0,
            "min_new_tokens": 500,
            "max_new_tokens": 1000,
        },
    )

    # Create message objects
    system_message = SystemMessage(content=system_prompt)
    user_prompt = f"Startup Info: {startup_info}\nInstagram Data: {instagram_data}"
    user_message = HumanMessage(content=user_prompt)

    # Generate response
    response = chat_model([system_message, user_message])

    # Parse the JSON response
    try:
        response_data = json.loads(response.content)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

    # Validate the parsed data using Pydantic
    try:
        validated_data = RedditInsights(**response_data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

    # Output the validated data
    print(validated_data.model_dump_json())
    return validated_data

# Function to get insights from Twitter data
def get_twitter_insights(startup_info, instagram_data):

    class TwitterInsights(BaseModel):
        platform: str = Field("Twitter/X", description="Social media platform name")
        market_trends: str = Field(..., description="Trending topics, viral discussions, and industry developments")
        customer_insights: str = Field(..., description="Pain points, discussions, and customer sentiment insights")
        competitive_landscape: str = Field(..., description="Competitors, influencers, and their engagement strategies")
        content_strategy: str = Field(..., description="Optimal types of tweets and engagement methods")
        marketing_tactics: str = Field(..., description="Strategies for visibility, advertising, and organic growth")


    system_prompt = """You are a market intelligence and audience growth strategist specializing in Twitter/X. 
        Your task is to analyze the startup’s description and the extracted Twitter/X discussions to generate **insightful and data-driven observations** about the market, customers, and industry landscape. 
        You will also provide **strategic recommendations** on how the startup can leverage these insights for marketing, audience growth, and brand positioning.

        ### Key Insights to Generate:
        1. **Industry & Market Trends** – What are the biggest emerging trends, innovations, and challenges in this industry? What new developments are shaping customer behavior?
        2. **Customer Sentiment & Pain Points** – Based on the Twitter data, what are customers discussing the most? What problems, frustrations, and unmet needs are recurring in conversations?
        3. **Competitive & Influencer Landscape** – What companies, startups, or influencers dominate the discussion? How do they engage with their audience, and what strategies work for them?
        4. **Content & Engagement Strategy** – What types of content (e.g., threads, polls, memes, case studies, expert opinions) resonate most with this audience? How should the startup position itself as a thought leader?
        5. **Marketing & Growth Strategies** – How can the startup attract its target audience on Twitter? What tactics, trends, and engagement strategies should be leveraged for sustainable brand growth?

        Important Note: If the provided Twitter/X data does not contain any significant or relevant info about one or more of the above points,
        you can generate hypothetical insights based on the startup description and general Twitter/X trends in the industry, as well as your own valid knowledge. 


        Output Format (JSON):
        {
        "platform": "Twitter/X",
        "market_trends": "...",
        "customer_insights": "...",
        "competitive_landscape": "...",
        "content_strategy": "...",
        "marketing_tactics": "..."
        }"""


    # Define model parameters
    chat_model = ChatWatsonx(
        model_id="ibm/granite-3-8b-instruct",
        url=url,
        apikey=watson_api_key,
        project_id=watson_project_id,
        params={
            "decoding_method": "greedy",
            "temperature": 0,
            "min_new_tokens": 500,
            "max_new_tokens": 1000,
        },
    )

    # Create message objects
    system_message = SystemMessage(content=system_prompt)
    user_prompt = f"Startup Info: {startup_info}\nInstagram Data: {instagram_data}"
    user_message = HumanMessage(content=user_prompt)

    # Generate response
    response = chat_model([system_message, user_message])

    # Parse the JSON response
    try:
        response_data = json.loads(response.content)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

    # Validate the parsed data using Pydantic
    try:
        validated_data = TwitterInsights(**response_data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

    # Output the validated data
    print(validated_data.model_dump_json())
    return validated_data

# Function to ask the AI agent a query
def ask_agent(query, startup_info):       
    # Define model parameters
    chat_model = ChatWatsonx(
        model_id="ibm/granite-3-8b-instruct",
        url=url,
        apikey=watson_api_key,
        project_id=watson_project_id,
        params={
            "decoding_method": "greedy",
            "temperature": 0,
            "min_new_tokens": 500,
            "max_new_tokens": 1000,
        },
    )

    @tool
    def vector_search(query: str) -> str:
        """Perform vector search to retrive context about Docling based on user query from the vector database.
            Args: search query : string
            Returns: retrieved context as a string
        """
        return query_db(query)
    
    # Initialize the TavilySearchAPIWrapper with the API key
    tavily_api_wrapper = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)

    # Initialize the TavilySearchResults tool with the API wrapper
    tavily_search_tool = TavilySearchResults(api_wrapper=tavily_api_wrapper, max_results=1)

    tools = [tavily_search_tool, vector_search]


    agent_executor = create_react_agent(chat_model, tools)

    response = agent_executor.invoke({"messages": f"""You are an AI assistant equipped with specialized tools to answer user queries.
            This is a description of the user's startup: {startup_info}
            - For questions related to the user's startup, use the 'vector_search' tool to fetch information from the vector database.
            - For all other generic queries, utilize the 'Tavily Search' tool to retrieve information from the web.
            - If the information from 'vector_search' is insufficient, you may also use 'Tavily Search' to supplement your response.\nUser query: {query}"""})

    res = response["messages"]
    print(res)

    # Extract the final AI-generated message content
    final_ai_message_content = None
    for message in reversed(res):
        if isinstance(message, AIMessage):
            final_ai_message_content = message.content
            break

    if final_ai_message_content:
        print(final_ai_message_content)
    else:
        print("No AI-generated message found.")

    return final_ai_message_content


