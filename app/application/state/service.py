from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.state import State
from app.infrastructure.repository import StateRepository
import pandas as pd
import io

class StateService:
    def __init__(self, repository: StateRepository):
        self.repository = repository

    def create_state(self, state: State) -> State:
        return self.repository.save(state)

    def get_states(self, skip: int = 0, limit: int = 100) -> List[State]:
        return self.repository.list(skip, limit)

    def get_state(self, id: int) -> Optional[State]:
        return self.repository.get_by_id(id)

    def update_state(self, id: int, state: State) -> Optional[State]:
        return self.repository.update(id, state)

    def delete_state(self, id: int) -> bool:
        return self.repository.delete(id)
    
    def delete_all_states(self):
        self.repository.delete_all()

    def upload_states(self, file_content: bytes, filename: str) -> int:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_content))
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError("Unsupported file format")

        states = []
        for _, row in df.iterrows():
            # Basic validation/cleaning could happen here
            state = State(
                id=None,
                code=str(row.get('code', '')),
                state=str(row.get('state', '')),
                capital=str(row.get('capital', '')),
                active=True
            )
            states.append(state)
        
        self.repository.bulk_save(states)
        return len(states)
