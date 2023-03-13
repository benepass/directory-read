import json

from chalicelib.services.handlers.extractors import extract_benepass


def test_extract_benepass_uploads_to_storage(
    uow,
    freeze,
    bucket,
    merge_roster,
    mocked_merge_roster_response,
):
    extract_benepass(uow)

    roster_data = list(bucket.objects.filter(Prefix="Benepass/2023-03-13/roster.json"))

    assert len(roster_data) == 1
    assert (
        json.loads(roster_data[0].get()["Body"].read().decode())
        == merge_roster["results"]
    )
