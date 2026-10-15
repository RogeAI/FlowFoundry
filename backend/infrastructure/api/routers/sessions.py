from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from application.attach_source import AttachSource
from application.start_session import StartSession
from application.set_wfg import SetWFG
from application.update_prompt import UpdatePrompt
from application.select_agent import SelectAgent
from application.update_actions import UpdateActions
from application.reset_session import ResetSession
from infrastructure.api.schemas.session import (
    SessionResponse,
    SourceResponse,
    UpdateActionsRequest,
    UpdatePromptRequest,
    SelectAgentRequest,
    SetWFGRequest,
)

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _to_response(session) -> SessionResponse:
    return SessionResponse(
        id=session.id,
        prompt=session.prompt,
        selected_actions=[a.label for a in session.selected_actions],
        selected_agent_id=session.selected_agent_id,
        wfg_active=session.wfg.active,
        expanded=session.expanded,
    )


@router.post("", response_model=SessionResponse)
def create_session(request: Request) -> SessionResponse:
    use_case = StartSession(request.app.state.session_repo)
    session = use_case.execute()
    return _to_response(session)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, request: Request) -> SessionResponse:
    session = request.app.state.session_repo.get_by_id(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return _to_response(session)


@router.get("/{session_id}/sources", response_model=list[SourceResponse])
def list_sources(session_id: str, request: Request) -> list[SourceResponse]:
    if request.app.state.session_repo.get_by_id(session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return [
        SourceResponse(
            source_id=source.source_id,
            original_filename=source.original_filename,
            source_type=source.source_type,
            size_bytes=source.size_bytes,
        )
        for source in request.app.state.source_repo.list_for_session(session_id)
    ]


@router.post("/{session_id}/sources", response_model=SourceResponse, status_code=201)
async def attach_source(
    session_id: str,
    request: Request,
    file: UploadFile = File(...),
) -> SourceResponse:
    try:
        content = await file.read(AttachSource.MAX_FILE_SIZE + 1)
        source = AttachSource(
            request.app.state.session_repo,
            request.app.state.source_repo,
            request.app.state.source_storage_root,
        ).execute(session_id, file.filename or "", content)
        return SourceResponse(
            source_id=source.source_id,
            original_filename=source.original_filename,
            source_type=source.source_type,
            size_bytes=source.size_bytes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await file.close()


@router.delete("/{session_id}/sources/{source_id}", status_code=204)
def delete_source(session_id: str, source_id: str, request: Request) -> None:
    if request.app.state.session_repo.get_by_id(session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if not request.app.state.source_repo.delete(session_id, source_id):
        raise HTTPException(status_code=404, detail="Session source not found")


@router.patch("/{session_id}/wfg", response_model=SessionResponse)
def set_wfg(
    session_id: str,
    body: SetWFGRequest,
    request: Request,
) -> SessionResponse:
    try:
        session = SetWFG(request.app.state.session_repo).execute(session_id, body.active)
        return _to_response(session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{session_id}/prompt", response_model=SessionResponse)
def update_prompt(
    session_id: str,
    body: UpdatePromptRequest,
    request: Request,
) -> SessionResponse:
    try:
        session = UpdatePrompt(request.app.state.session_repo).execute(
            session_id,
            body.prompt,
        )
        return _to_response(session)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/{session_id}/agent", response_model=SessionResponse)
def select_agent(session_id: str, body: SelectAgentRequest, request: Request) -> SessionResponse:
    try:
        use_case = SelectAgent(request.app.state.session_repo, request.app.state.agent_repo)
        session = use_case.execute(session_id, body.agent_id)
        return _to_response(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{session_id}/actions", response_model=SessionResponse)
def update_actions(session_id: str, body: UpdateActionsRequest, request: Request) -> SessionResponse:
    try:
        use_case = UpdateActions(request.app.state.session_repo)
        session = use_case.execute(session_id, body.actions)
        return _to_response(session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{session_id}")
def reset_session(session_id: str, request: Request) -> SessionResponse:
    try:
        use_case = ResetSession(
            request.app.state.session_repo,
            request.app.state.source_repo,
        )
        session = use_case.execute(session_id)
        return _to_response(session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
