from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from src.listing_models import Brand, GuitarDetails

current_folder = Path(__file__).parent


@pytest.mark.parametrize(
    "filepath,brand,expected_raw",
    [
        pytest.param(
            "./pages/epiphone-bb-king-lucille-cherry.html",
            Brand.epiphone,
            {
                "Body Style": "ES",
                "Body Shape": "ES-335",
                "Body Material": "5-ply Maple/Poplar",
                "Bracing": "Spruce",
                "Centerblock": "Maple",
                "Binding": "Multi-ply Top, Back, and Headstock, Single ply Neck",
                "Body Finish": "Gloss",
                "Profile": 'Rounded "C"',
                "Scale Length": "628.65 mm / 24.75 in",
                "Fingerboard Material": "Ebony",
                "Fingerboard Radius": "304.8 mm / 12 in",
                "Fret Count": "22",
                "Frets": " Medium Jumbo",
                "Nut Material": "Graph Tech",
                "Nut Width": "43.0 mm / 1.692 in",
                "Inlays": " Pearloid Blocks",
                "Joint": "Glued In, Set Neck",
                "Finish": "Gold",
                "Bridge": "Epiphone LockTone Tune-O-Matic",
                "Tailpiece": "TP-6 Stop Bar with Fine Tuners",
                "Tuning Machines": "Grover Rotomatic with Keystone Buttons",
                "Pickguard": "5-ply ES-335 style Bound Tortoise Pickguard ",
                "Truss Rod": "2-way Adjustable",
                "Truss Rod Cover": 'Brass Bell; Engraved "B.B. King"',
                "Control Knobs": "Black Speed Knobs, Black Chicken Head Varitone Knob",
                "Switch Tip": "Cream",
                "Switch washer": "Gold Varitone Washer",
                "Control Covers": "Black; PVC",
                "Strap Buttons": "2 - Bottom and Back of Heel ",
                "Mounting Rings": "Black",
                "Pickup Covers": "Gold",
                "Neck Pickup": "Alnico Classic PRO",
                "Bridge Pickup": "Alnico Classic PRO",
                "Controls": "2 Volume, 2 Tone, CTS Potentiometers, 6 Position Varitone Switch",
                "Pickup Selector": "3-way Epiphone Toggle",
                "Output Jack": 'Two: Epiphone 1/4" Mono and Epiphone 1/4" Stereo ',
                "Strings Gauge": " .010, .013, .017, .026, .036, .046",
                "Case": "EpiLite Case Included",
                "finishes": "Cherry",
                "brand": "Epiphone",
                "url": "https://example.com",
                "model": "B.B. King Lucille,\n                            Exclusive",
            },
            id="BB King Lucille Cherry",
        ),
    ],
)
def test_GuitarDetails_get(filepath: str, brand: Brand, expected_raw: dict):
    expected = GuitarDetails(**expected_raw)
    file_ = current_folder / Path(filepath)
    soup = BeautifulSoup(file_.read_text(), features="html.parser")
    res = GuitarDetails.get(soup, brand, "https://example.com")
    assert res == expected
