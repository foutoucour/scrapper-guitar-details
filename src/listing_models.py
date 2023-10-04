from __future__ import annotations

from enum import Enum
from typing import List, Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


class Listing(BaseModel):
    guitars: List[GuitarDetails]


class GuitarDetails(BaseModel):
    body__style: Optional[str] = Field(None, alias="Body Style")
    body__shape: Optional[str] = Field(None, alias="Body Shape")
    body__material: Optional[str] = Field(None, alias="Body Material")
    top: Optional[str] = Field(None, alias="Top")
    back: Optional[str] = Field(None, alias="Back")
    side: Optional[str] = Field(None, alias="Side")
    centerblock: Optional[str] = Field(None, alias="Centerblock")
    binding: Optional[str] = Field(None, alias="Binding")
    body__finish: Optional[str] = Field(None, alias="Body Finish")
    profile: Optional[str] = Field(None, alias="Profile")
    scale__length: Optional[str] = Field(None, alias="Scale Length")
    fingerboard__material: Optional[str] = Field(None, alias="Fingerboard Material")
    fingerboard__radius: Optional[str] = Field(None, alias="Fingerboard Radius")
    fret__count: Optional[str] = Field(None, alias="Fret Count")
    frets: Optional[str] = Field(None, alias="Frets")
    nut__material: Optional[str] = Field(None, alias="Nut Material")
    nut__width: Optional[str] = Field(None, alias="Nut Width")
    end__of__board__width: Optional[str] = Field(None, alias="End Of Board Width")
    inlays: Optional[str] = Field(None, alias="Inlays")
    joint: Optional[str] = Field(None, alias="Joint")
    finish: Optional[str] = Field(None, alias="Finish")
    bridge: Optional[str] = Field(None, alias="Bridge")
    tailpiece: Optional[str] = Field(None, alias="Tailpiece")
    tuning__machines: Optional[str] = Field(None, alias="Tuning Machines")
    pickguard: Optional[str] = Field(None, alias="Pickguard")
    truss__rod: Optional[str] = Field(None, alias="Truss Rod")
    truss__rod__cover: Optional[str] = Field(None, alias="Truss Rod Cover")
    control__knobs: Optional[str] = Field(None, alias="Control Knobs")
    switch__tip: Optional[str] = Field(None, alias="Switch Tip")
    strap__buttons: Optional[str] = Field(None, alias="Strap Buttons")
    mounting__rings: Optional[str] = Field(None, alias="Mounting Rings")
    pickup__covers: Optional[str] = Field(None, alias="Pickup Covers")
    neck__pickup: Optional[str] = Field(None, alias="Neck Pickup")
    bridge__pickup: Optional[str] = Field(None, alias="Bridge Pickup")
    controls: Optional[str] = Field(None, alias="Controls")
    pickup__selector: Optional[str] = Field(None, alias="Pickup Selector")
    output__jack: Optional[str] = Field(None, alias="Output Jack")
    strings__gauge: Optional[str] = Field(None, alias="Strings Gauge")
    case: Optional[str] = Field(None, alias="Case")
    model: Optional[str] = None
    finishes: Optional[str] = None
    brand: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def get(cls, soup: BeautifulSoup, brand: Brand, link: str) -> GuitarDetails:
        master = soup.find("div", id="master-product-tab-content")
        h6 = master.find_all("h6")
        raw_details = {h.getText(): h.find_next("p").getText() for h in h6}
        details = cls(**raw_details)
        details.set_finishes(soup, brand)
        details.set_model(soup)
        details.brand = brand.value
        details.url = link
        return details

    def set_model(self, soup: BeautifulSoup) -> None:
        self.model = soup.find("h2").getText()

    def set_finishes(self, soup: BeautifulSoup, brand: Brand) -> None:
        if brand == Brand.gibson:
            finishes = [
                finish.get("aria-label")
                for finish in soup.find_all("a", class_="singleFinish")
            ]
        else:
            finishes = [
                finish.get("aria-label")
                for finish in soup.find_all("label", class_="rs-finish-button")
            ]
        self.finishes = ";".join(finishes)


class Brand(Enum):
    gibson = "Gibson"
    epiphone = "Epiphone"
