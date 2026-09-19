from classpad.core.models import HistoryEntry, Session
from classpad.core.persistence import SessionStore
def test_session_round_trip(tmp_path):
    session=Session(); session.variables["x"]="5"; session.history.append(HistoryEntry("Main","2+3","5","5.0","2+3"))
    SessionStore(tmp_path/"state.json").save(session); loaded=SessionStore(tmp_path/"state.json").load()
    assert loaded.variables == {"x":"5"}; assert loaded.history[0].exact_text == "5"
