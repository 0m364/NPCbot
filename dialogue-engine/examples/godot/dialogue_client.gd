extends Node

const DIALOGUE_URL := "http://127.0.0.1:8787/v1/dialogue/generate"

var http: HTTPRequest


func _ready() -> void:
    http = HTTPRequest.new()
    add_child(http)
    http.request_completed.connect(_on_request_completed)


func request_dialogue(player_text: String) -> void:
    var payload := {
        "npc_id": "OutpostGuide",
        "player_input": player_text,
        "npc_persona": "Calm, tactical, protective",
        "world_state": "Outpost in partial lockdown",
        "quest_state": "Escort mission active",
        "tone": "grounded, cinematic",
        "constraints": "Teen-safe, concise"
    }
    var headers := PackedStringArray(["Content-Type: application/json"])
    var err := http.request(DIALOGUE_URL, headers, HTTPClient.METHOD_POST, JSON.stringify(payload))
    if err != OK:
        push_warning("Dialogue request failed to start.")


func _on_request_completed(_result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code != 200:
        push_warning("Dialogue error code: %d" % response_code)
        return

    var parsed: Variant = JSON.parse_string(body.get_string_from_utf8())
    if typeof(parsed) != TYPE_DICTIONARY:
        push_warning("Dialogue response parse failed")
        return

    var text: String = str(parsed.get("dialogue", ""))
    print("Dialogue:\n", text)
