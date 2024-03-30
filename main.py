from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import DefaultDict, Optional, List
import pandas as pd

app = FastAPI()


class Position(Enum):
    DEFENDER = 'defender'
    MIDFIELDER = 'midfielder'
    FORWARD = 'forward'


class Skills(Enum):
    DEFENSE = 'defense'
    ATTACK = 'attack'
    SPEED = 'speed'
    STRENGTH = 'strength'
    STAMINA = 'stamina'


class Skill(BaseModel):
    name: Skills
    value: Optional[float] = None


class Player(BaseModel):
    id: int
    name: str
    position: Position
    skills: DefaultDict[Skills, float]


data = pd.read_csv('data_players.csv')[:15]
players = {}
for i, r in data.iterrows():
    skills = {Skills.ATTACK: r['attack'],
              Skills.DEFENSE: r['defense'],
              Skills.SPEED: r['speed'],
              Skills.STAMINA: r['stamina'],
              Skills.STRENGTH: r['strength']}
    players[i] = Player(id=i,
                        name=r['name'],
                        position=r['position'],
                        skills=skills)


# return / list all players
@app.get("/")
def index() -> dict[str, dict[int, Player]]:
    return {"players": players}


# return specific player
@app.get("/players/{player_id}")
def query_player_by_id(player_id: int) -> Player:

    if player_id not in players:
        HTTPException(status_code=404,
                      detail=f"Player with {player_id=} does not exist.")

    return players[player_id]


# add player
@app.post("/")
def add_player(player: Player) -> dict[str, Player]:

    if player.id in players:
        HTTPException(status_code=400,
                      detail=f"Player with {player.id=} already exists.")

    players[player.id] = player
    return {"added": player}


# update player
@app.put("/update/{player_id}")
def update(
    player_id: int,
    name: Optional[str] = None,
    position: Optional[str] = None,
    skills: Optional[dict] = None
) -> dict[str, Player]:

    if player_id not in players:
        HTTPException(status_code=404,
                      detail=f"Player with {player_id=} does not exist.")
    if all(info is None for info in (name, position, skills)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    player = players[player_id]
    if name is not None:
        player.name = name
    if position is not None:
        player.position = position
    if skills is not None:
        player.skills = skills

    return {"updated": player}


# delete a player
@app.delete("/delete/{player_id}")
def delete_player(player_id: int) -> dict[str, Player]:

    if player_id not in players:
        raise HTTPException(
            status_code=404, detail=f"Player with {player_id=} does not exist."
        )

    player = players.pop(player_id)
    return {"deleted": player}


Selection = dict[
    str, Position | Skills | None
]  # dictionary containing the user's query arguments


# query by parameters
@app.get("/players/")
def query_player_by_parameters(
    position: Position | None = None,
    skill: Skills | None = None,
) -> dict[str, Selection | Player]:
    def check_player(player: Player):
        """Check if the player matches the query arguments"""
        return all(
            (
                position is None or player.position is position,
                skill is None or player.skills[skill] > 0,
            )
        )
    selection = [player for player in players.values() if check_player(player)]
    value = max([p.skills[skill] for p in selection])
    selection = [p for p in selection if p.skills[skill] == value]
    return {
        "query": {"position": position,
                  "skill": skill,
                  },
        "selection": selection[0],
    }


@app.get("/best/")
def query_best(
    skill: Skills,
    pos: List[Position] = Query(None),
):
    out = []
    for p in pos:
        selection = [player for player in players.values()
                     if player.position is p]
        value = max([p.skills[skill] for p in selection])
        selection = [p for p in selection if p.skills[skill] == value]
        out.append(selection[0])
    return {
        "skill": skill,
        "selection": out}
