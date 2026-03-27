from sqlalchemy.orm import Session, aliased
from database import SessionLocal
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException, status
from fastapi.responses import RedirectResponse
import models, schemas
import boto3
import jwt
from datetime import datetime
import requests
import math
import os
import random
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from agents import RunConfig, ModelSettings, InputGuardrail, OutputGuardrail
from agent_manager import (
    get_provider_client,
    MaysonAgentModelProvider,
    run_agent_query,
    AgentBaseDto,
    create_agent,
    guardrail_pii,
    guardrail_profanity,
    guardrail_length,
    guardrail_violence,
    guardrail_latency,
    tool_scraper,
    tool_reader,
    tool_weather,
    tool_summarize,
    tool_checker,
    tool_csv,
)


load_dotenv()


def convert_to_datetime(date_string):
    if date_string is None:
        return datetime.now()
    if not date_string.strip():
        return datetime.now()
    if "T" in date_string:
        try:
            return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        except ValueError:
            date_part = date_string.split("T")[0]
            try:
                return datetime.strptime(date_part, "%Y-%m-%d")
            except ValueError:
                return datetime.now()
    else:
        # Try to determine format based on first segment
        parts = date_string.split("-")
        if len(parts[0]) == 4:
            # Likely YYYY-MM-DD format
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                return datetime.now()

        # Try DD-MM-YYYY format
        try:
            return datetime.strptime(date_string, "%d-%m-%Y")
        except ValueError:
            return datetime.now()

        # Fallback: try YYYY-MM-DD if not already tried
        if len(parts[0]) != 4:
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                return datetime.now()

        return datetime.now()


async def get_agent(request: Request, db: Session, prompt: str):

    # darfae

    client = get_provider_client(
        api_provider="OPENROUTER",
        api_key=os.getenv("key_728d80120e3c4f8d85c4c4a931336a45"),
    )
    print("client:", client)
    provider = MaysonAgentModelProvider(client)
    print("provider:", provider)
    run_config = RunConfig(
        model="""z-ai/glm-4.5-air""",
        model_provider=provider,
        model_settings=ModelSettings(temperature=0.7),
    )

    print("run_config:", run_config)
    tendua_agent = create_agent(
        dto=AgentBaseDto(
            agent_name="""tendua""",
            agent_description="",
            model_name="""z-ai/glm-4.5-air""",
            system_prompt="""You are a veteran Software Architect with 15+ years of experience. You’ve seen Strategy and Observer patterns used as band-aids for hemorrhaging codebases. You value DRY, SOLID, and KISS above all else. You have zero patience for high coupling, "god objects," or logic that breaks the moment a new requirement is added""",
            temperature=0.7,
            input_guardrails=[InputGuardrail(guardrail_function=guardrail_profanity)],
            output_guardrails=[],
            tools=[],
        )
    )
    print("agent:", tendua_agent)

    try:
        agent_response = await asyncio.wait_for(
            run_agent_query(agent=tendua_agent, query=prompt, run_config=run_config),
            timeout=120,  # 2 minutes
        )
    except asyncio.TimeoutError:
        return {
            "status": 504,
            "message": "Agent timed out after 2 minutes.",
            "data": {"response": None},
        }
    print("return_variable_name", agent_response)

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"response": agent_response},
    }
    return res
