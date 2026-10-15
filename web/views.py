import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .services import build_local_session, get_agent_cards, prepare_local_workflow, resolve_local_attention


STEPS = [
    ("01", "Describe the outcome", "Start with the result you want, in your own words. Add useful actions, files, or a preferred specialist only when they help."),
    ("02", "ForgeMaster prepares the flow", "ForgeMaster reviews the request, asks when something is unclear, and decides which specialist Agents should contribute and in what order."),
    ("03", "Specialists do the focused work", "One Agent may be enough, or several can work in sequence or together. Each stays focused on its declared specialty."),
    ("04", "Follow the work to a result", "See the plan, respond when input is needed, and keep the full objective and its progress together in one workspace."),
]

CAPABILITIES = [
    ("✦", "Start naturally", "You do not need to know the Agent catalogue. Explain what you want to achieve and FlowFoundry helps shape the path."),
    ("▤", "Bring your context", "Attach relevant source material so the work begins with the information that matters."),
    ("◈", "Use the right specialists", "Express a preference or let ForgeMaster identify the most suitable Agent combination for the outcome."),
    ("◎", "Stay oriented", "Keep the plan, participating Agents, progress, questions, and outputs connected to the same objective."),
    ("Ⅱ", "Pause before execution", "Use Wait for GO when you want to prepare the request now and release it only when you are ready."),
    ("↻", "Keep oversight", "ForgeMaster remains present throughout, receiving escalations and adjusting the flow when circumstances change."),
]

ACTIONS = ["Summarize", "Review requirements", "Create testable scenarios", "Design test cases", "Identify gaps", "Compare documents"]

def about(request):
    return render(request, "web/about.html", {"steps": STEPS, "capabilities": CAPABILITIES})


def workspace(request):
    return render(request, "web/workspace.html", {"actions": ACTIONS, "agents": get_agent_cards()})


def session(request):
    return render(request, "web/session.html", {"session_data": build_local_session(), "agents": get_agent_cards()})


@require_POST
def prepare_workflow(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "The workflow request was not valid JSON."}, status=400)

    objective = str(payload.get("objective", ""))
    actions = [str(action) for action in payload.get("actions", []) if str(action) in ACTIONS]
    preferred_agent = payload.get("preferred_agent")
    valid_agent_ids = {agent["id"] for agent in get_agent_cards() if agent["status"] == "Available"}
    if preferred_agent not in valid_agent_ids:
        preferred_agent = None
    return JsonResponse(
        prepare_local_workflow(
            objective=objective,
            actions=actions,
            preferred_agent=preferred_agent,
            wfg_active=payload.get("wfg_active") is True,
        )
    )


@require_POST
def respond_to_session(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "The session response was not valid JSON."}, status=400)
    return JsonResponse(resolve_local_attention(response=str(payload.get("response", ""))))
