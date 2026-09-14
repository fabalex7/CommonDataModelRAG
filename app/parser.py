import json
from pathlib import Path

def flatten_cdm(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    chunks = []

    for definition in data.get("definitions", []):
        entity_name = definition.get("entityName")
        if not entity_name:
            continue
        entity_description = definition.get("description", "")

        chunks.append({
            "text": (
                f"Entity: {entity_name}\n"
                f"Description: {entity_description}\n"
                f"Extends: {definition.get('extendsEntity', '')}"
            ),
            "metadata": {
                "entity": entity_name,
                "kind": "entity",
                "name": entity_name,
                "source_name": entity_name,
                "description": entity_description,
            },
        })

        for attribute_group in definition.get("hasAttributes", []):
            if not isinstance(attribute_group, dict):
                continue

            attribute_group_reference = attribute_group.get(
                "attributeGroupReference"
            )
            if isinstance(attribute_group_reference, dict):
                members = attribute_group_reference.get("members", [])
            elif "members" in attribute_group:
                members = attribute_group.get("members", [])
            else:
                members = [attribute_group]

            for member in members:
                if not isinstance(member, dict):
                    continue
                name = member.get("name")
                source_name = member.get("sourceName", name)
                display_name = member.get("displayName", name)
                description = member.get("description", "")
                data_type = member.get("dataType", "")
                purpose = member.get("purpose", "")

                if isinstance(data_type, dict):
                    data_type = data_type.get("dataTypeReference", "")

                entity = member.get("entity")
                if entity:
                    if isinstance(entity, str):
                        target = entity
                    else:
                        target = entity.get("entityReference", "")
                        if isinstance(target, dict):
                            target = target.get("entityName", "")
                    foreign_key = (
                        member.get("resolutionGuidance", {})
                        .get("entityByReference", {})
                        .get("foreignKeyAttribute", {})
                    )

                    text = (
                        f"Entity {entity_name} has relationship '{name}' "
                        f"to entity '{target}'. "
                        f"Source column: {source_name}. "
                        f"Foreign key: {foreign_key.get('sourceName', source_name)}. "
                        f"Description: {description}"
                    )

                    chunks.append({
                        "text": text,
                        "metadata": {
                            "entity": entity_name,
                            "kind": "relationship",
                            "name": name,
                            "target_entity": target,
                            "source_name": source_name,
                        },
                    })
                    continue

                text = (
                    f"Entity: {entity_name}\n"
                    f"Attribute: {name}\n"
                    f"Display name: {display_name}\n"
                    f"Source column: {source_name}\n"
                    f"Data type: {data_type}\n"
                    f"Purpose: {purpose}\n"
                    f"Description: {description}"
                )

                chunks.append({
                    "text": text,
                    "metadata": {
                        "entity": entity_name,
                        "kind": "attribute",
                        "name": name,
                        "source_name": source_name,
                        "data_type": str(data_type),
                    },
                })

    return chunks