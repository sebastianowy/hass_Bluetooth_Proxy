entity_id = data.get("entity_id")
state = data.get("state", "unknown")
attributes = data.get("attributes", {})

if entity_id is not None:
    hass.states.set(entity_id, state, attributes)