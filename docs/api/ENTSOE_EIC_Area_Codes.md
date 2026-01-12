# ENTSO-E Energy Identification Codes (EIC) - Area List

This document provides a comprehensive reference for Energy Identification Codes (EIC) used in the ENTSO-E Transparency Platform API.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Area Type Definitions](#2-area-type-definitions)
3. [EIC Codes by Country](#3-eic-codes-by-country)
4. [EIC Codes by Area Type](#4-eic-codes-by-area-type)
5. [Quick Reference Tables](#5-quick-reference-tables)
6. [Special Codes and Interconnections](#6-special-codes-and-interconnections)

---

## 1. Overview

### What is an EIC Code?

An **Energy Identification Code (EIC)** is a unique identifier used across the European energy sector to identify:
- Market participants
- Geographic areas
- Measurement points
- Resources

EIC codes are essential for API queries on the ENTSO-E Transparency Platform as they uniquely identify the areas for which data is requested.

### EIC Code Format

EIC codes follow a standard 16-character format:
- Positions 1-2: Object type identifier (e.g., "10" for areas)
- Position 3: Check character type
- Positions 4-15: Unique identifier
- Position 16: Check character

**Example:** `10YFR-RTE------C` (France)

---

## 2. Area Type Definitions

The following area types are used in the ENTSO-E Transparency Platform:

| Code | Area Type | Description |
|------|-----------|-------------|
| **BZN** | Bidding Zone | The largest geographical area within which Market Participants are able to exchange energy without Capacity Allocation |
| **BZA** | Bidding Zone Aggregation | An aggregation of multiple bidding zones |
| **CTA** | Control Area | A coherent part of the interconnected system, operated by a single system operator and shall include connected physical loads and/or generation units if any |
| **MBA** | Market Balance Area | A geographic area consisting of one or more Metering Grid Areas with common market rules for which the settlement responsible party carries out a balance settlement and which has the same price for imbalance |
| **IBA** | Imbalance Area | The Imbalance Price Area or a part of an Imbalance Price Area, for the calculation of an Imbalance |
| **IPA** | Imbalance Price Area | Either a Bidding Zone, part of a Bidding Zone or a combination of several Bidding Zones, defined by each TSO for the purpose of calculation of Imbalance Prices |
| **LFA** | Load Frequency Control Area | Area for load frequency control purposes |
| **LFB** | Load Frequency Control Block | The composition of one or more Control Areas, working together to ensure the load frequency control on behalf of RGCE |
| **REG** | Region | A regional grouping of areas |
| **SCA** | Scheduling Area | The Bidding Zone except if there is more than one Responsibility Area within this Bidding Zone. In the latter case, the Scheduling Area equals Responsibility Area or a group of Responsibility Areas |
| **SNA** | Synchronous Area | An area covered by interconnected Transmission System Operators (TSOs) with a common System Frequency in a steady state |

---

## 3. EIC Codes by Country

### Albania (AL)
| EIC Code | Area Types |
|----------|------------|
| `10YAL-KESH-----5` | BZN\|AL, CTA\|AL, MBA\|AL, LFA\|AL, LFB\|AL, SCA\|AL |

### Armenia (AM)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001B004` | BZN\|AM, CTA\|AM |

### Austria (AT)
| EIC Code | Area Types |
|----------|------------|
| `10YAT-APG------L` | BZN\|AT, CTA\|AT, MBA\|AT, IPA\|AT, LFA\|AT, LFB\|AT, SCA\|AT |

### Azerbaijan (AZ)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001B05V` | BZN\|AZ, CTA\|AZ |

### Belarus (BY)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A51S` | BZN\|BY, CTA\|BY, MBA\|BY, SCA\|BY |

### Belgium (BE)
| EIC Code | Area Types |
|----------|------------|
| `10YBE----------2` | BZN\|BE, CTA\|BE, MBA\|BE, LFA\|BE, LFB\|BE, SCA\|BE |

### Bosnia and Herzegovina (BA)
| EIC Code | Area Types |
|----------|------------|
| `10YBA-JPCC-----D` | BZN\|BA, CTA\|BA, MBA\|BA, LFA\|BA, SCA\|BA |

### Bulgaria (BG)
| EIC Code | Area Types |
|----------|------------|
| `10YCA-BULGARIA-R` | BZN\|BG, CTA\|BG, MBA\|BG, LFA\|BG, LFB\|BG, SCA\|BG |

### Croatia (HR)
| EIC Code | Area Types |
|----------|------------|
| `10YHR-HEP------M` | BZN\|HR, CTA\|HR, MBA\|HR, LFA\|HR, SCA\|HR |

### Cyprus (CY)
| EIC Code | Area Types |
|----------|------------|
| `10YCY-1001A0003J` | BZN\|CY, CTA\|CY, MBA\|CY, SCA\|CY |

### Czech Republic (CZ)
| EIC Code | Area Types |
|----------|------------|
| `10YCZ-CEPS-----N` | BZN\|CZ, CTA\|CZ, MBA\|CZ, LFA\|CZ, LFB\|CZ, SCA\|CZ |

### Denmark (DK)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A65H` | Denmark (general) |
| `10Y1001A1001A796` | CTA\|DK |
| `10YDK-1--------W` | BZN\|DK1, IBA\|DK1, IPA\|DK1, LFA\|DK1, MBA\|DK1, SCA\|DK1 |
| `10YDK-1-------AA` | BZN\|DK1A |
| `10YDK-2--------M` | BZN\|DK2, IBA\|DK2, IPA\|DK2, LFA\|DK2, MBA\|DK2, SCA\|DK2 |

### Estonia (EE)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A39I` | BZN\|EE, CTA\|EE, MBA\|EE, SCA\|EE |

### Finland (FI)
| EIC Code | Area Types |
|----------|------------|
| `10YFI-1--------U` | BZN\|FI, CTA\|FI, MBA\|FI, IBA\|FI, IPA\|FI, SCA\|FI |

### France (FR)
| EIC Code | Area Types |
|----------|------------|
| `10YFR-RTE------C` | BZN\|FR, CTA\|FR, MBA\|FR, LFA\|FR, LFB\|FR, SCA\|FR |

### Georgia (GE)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001B012` | BZN\|GE, CTA\|GE, MBA\|GE, SCA\|GE |

### Germany (DE)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A83F` | IPA\|DE, Germany (general) |
| `10Y1001A1001A82H` | BZN\|DE-LU, IPA\|DE-LU, MBA\|DE-LU, SCA\|DE-LU |
| `10Y1001A1001A63L` | BZN\|DE-AT-LU |
| `10YDE-ENBW-----N` | CTA\|DE(TransnetBW), LFA\|DE(TransnetBW), SCA\|DE(TransnetBW) |
| `10YDE-EON------1` | CTA\|DE(TenneT GER), LFA\|DE(TenneT GER), SCA\|DE(TenneT GER) |
| `10YDE-RWENET---I` | CTA\|DE(Amprion), LFA\|DE(Amprion), SCA\|DE(Amprion) |
| `10YDE-VE-------2` | CTA\|DE(50Hertz), LFA\|DE(50Hertz), SCA\|DE(50Hertz), BZA\|DE(50HzT) |
| `10Y1001C--00002H` | LFA\|DE(Amprion)-LU, SCA\|DE(Amprion)-LU |
| `10YCB-GERMANY--8` | LFB\|DE_DK1_LU, SCA\|DE_DK1_LU |

### Greece (GR)
| EIC Code | Area Types |
|----------|------------|
| `10YGR-HTSO-----Y` | BZN\|GR, CTA\|GR, MBA\|GR, LFA\|GR, LFB\|GR, SCA\|GR |

### Hungary (HU)
| EIC Code | Area Types |
|----------|------------|
| `10YHU-MAVIR----U` | BZN\|HU, CTA\|HU, MBA\|HU, LFA\|HU, LFB\|HU, SCA\|HU |

### Ireland (IE) / Northern Ireland (NIE)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A59C` | BZN\|IE(SEM), MBA\|IE(SEM), SCA\|IE(SEM), LFB\|IE-NIE, SNA\|Ireland |
| `10YIE-1001A00010` | CTA\|IE, MBA\|SEM(EirGrid), SCA\|IE |
| `10Y1001A1001A016` | CTA\|NIE, MBA\|SEM(SONI), SCA\|NIE |

### Italy (IT)
| EIC Code | Area Types |
|----------|------------|
| `10YIT-GRTN-----B` | CTA\|IT, LFA\|IT, LFB\|IT, MBA\|IT, SCA\|IT |
| `10Y1001A1001A73I` | BZN\|IT-North, MBA\|IT-Z-North, SCA\|IT-North |
| `10Y1001A1001A70O` | BZN\|IT-Centre-North, MBA\|IT-Z-Centre-North, SCA\|IT-Centre-North |
| `10Y1001A1001A71M` | BZN\|IT-Centre-South, MBA\|IT-Z-Centre-South, SCA\|IT-Centre-South |
| `10Y1001A1001A788` | BZN\|IT-South, MBA\|IT-Z-South, SCA\|IT-South |
| `10Y1001A1001A74G` | BZN\|IT-Sardinia, MBA\|IT-Z-Sardinia, SCA\|IT-Sardinia |
| `10Y1001A1001A75E` | BZN\|IT-Sicily, MBA\|IT-Z-Sicily, SCA\|IT-Sicily |
| `10Y1001A1001A699` | BZN\|IT-Brindisi, MBA\|IT-Z-Brindisi, SCA\|IT-Brindisi |
| `10Y1001A1001A72K` | BZN\|IT-Foggia, MBA\|IT-Z-Foggia, SCA\|IT-Foggia |
| `10Y1001A1001A76C` | BZN\|IT-Priolo, MBA\|IT-Z-Priolo, SCA\|IT-Priolo |
| `10Y1001A1001A77A` | BZN\|IT-Rossano, MBA\|IT-Z-Rossano, SCA\|IT-Rossano |
| `10Y1001C--00096J` | BZN\|IT-Calabria, MBA\|IT-Z-Calabria, SCA\|IT-Calabria |
| `10Y1001A1001A84D` | MBA\|IT-MACRZONENORTH, SCA\|IT-MACRZONENORTH |
| `10Y1001A1001A85B` | MBA\|IT-MACRZONESOUTH, SCA\|IT-MACRZONESOUTH |
| `10Y1001A1001A80L` | BZN\|IT-North-AT |
| `10Y1001A1001A81J` | BZN\|IT-North-FR |
| `10Y1001A1001A67D` | BZN\|IT-North-SI |
| `10Y1001A1001A68B` | BZN\|IT-North-CH |
| `10Y1001A1001A66F` | BZN\|IT-GR |
| `10Y1001A1001A877` | BZN\|IT-Malta |
| `10Y1001A1001A885` | BZN\|IT-SACOAC |
| `10Y1001A1001A893` | BZN\|IT-SACODC, SCA\|IT-SACODC |

### Kosovo (XK)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001C--00100H` | BZN\|XK, CTA\|XK, LFA\|XK, LFB\|XK, MBA\|XK |

### Latvia (LV)
| EIC Code | Area Types |
|----------|------------|
| `10YLV-1001A00074` | BZN\|LV, CTA\|LV, MBA\|LV, SCA\|LV |

### Lithuania (LT)
| EIC Code | Area Types |
|----------|------------|
| `10YLT-1001A0008Q` | BZN\|LT, CTA\|LT, MBA\|LT, SCA\|LT |

### Luxembourg (LU)
| EIC Code | Area Types |
|----------|------------|
| `10YLU-CEGEDEL-NQ` | CTA\|LU |

### Malta (MT)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A93C` | BZN\|MT, CTA\|MT, MBA\|MT, SCA\|MT |

### Moldova (MD)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A990` | BZN\|MD, CTA\|MD, LFA\|MD, MBA\|MD, SCA\|MD |

### Montenegro (ME)
| EIC Code | Area Types |
|----------|------------|
| `10YCS-CG-TSO---S` | BZN\|ME, CTA\|ME, MBA\|ME, LFA\|ME, SCA\|ME |

### Netherlands (NL)
| EIC Code | Area Types |
|----------|------------|
| `10YNL----------L` | BZN\|NL, CTA\|NL, MBA\|NL, LFA\|NL, LFB\|NL, SCA\|NL |

### North Macedonia (MK)
| EIC Code | Area Types |
|----------|------------|
| `10YMK-MEPSO----8` | BZN\|MK, CTA\|MK, MBA\|MK, LFA\|MK, SCA\|MK |

### Norway (NO)
| EIC Code | Area Types |
|----------|------------|
| `10YNO-0--------C` | CTA\|NO, MBA\|NO, SCA\|NO |
| `10YNO-1--------2` | BZN\|NO1, IBA\|NO1, IPA\|NO1, MBA\|NO1, SCA\|NO1 |
| `10Y1001A1001A64J` | BZN\|NO1A |
| `10YNO-2--------T` | BZN\|NO2, IBA\|NO2, IPA\|NO2, MBA\|NO2, SCA\|NO2 |
| `10Y1001C--001219` | BZN\|NO2A |
| `10YNO-3--------J` | BZN\|NO3, IBA\|NO3, IPA\|NO3, MBA\|NO3, SCA\|NO3 |
| `10YNO-4--------9` | BZN\|NO4, IBA\|NO4, IPA\|NO4, MBA\|NO4, SCA\|NO4 |
| `10Y1001A1001A48H` | BZN\|NO5, IBA\|NO5, IPA\|NO5, MBA\|NO5, SCA\|NO5 |

### Poland (PL)
| EIC Code | Area Types |
|----------|------------|
| `10YPL-AREA-----S` | BZN\|PL, BZA\|PL, CTA\|PL, MBA\|PL, LFA\|PL, SCA\|PL |
| `10YCB-POLAND---Z` | LFB\|PL |

### Portugal (PT)
| EIC Code | Area Types |
|----------|------------|
| `10YPT-REN------W` | BZN\|PT, CTA\|PT, MBA\|PT, LFA\|PT, LFB\|PT, SCA\|PT |

### Romania (RO)
| EIC Code | Area Types |
|----------|------------|
| `10YRO-TEL------P` | BZN\|RO, CTA\|RO, MBA\|RO, LFA\|RO, LFB\|RO, SCA\|RO |

### Russia (RU)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A49F` | BZN\|RU, CTA\|RU, MBA\|RU, SCA\|RU |
| `10Y1001A1001A50U` | BZN\|RU-KGD, CTA\|RU-KGD, MBA\|RU-KGD, SCA\|RU-KGD |

### Serbia (RS)
| EIC Code | Area Types |
|----------|------------|
| `10YCS-SERBIATSOV` | BZN\|RS, CTA\|RS, MBA\|RS, LFA\|RS, SCA\|RS |

### Slovakia (SK)
| EIC Code | Area Types |
|----------|------------|
| `10YSK-SEPS-----K` | BZN\|SK, CTA\|SK, MBA\|SK, LFA\|SK, LFB\|SK, SCA\|SK |

### Slovenia (SI)
| EIC Code | Area Types |
|----------|------------|
| `10YSI-ELES-----O` | BZN\|SI, CTA\|SI, MBA\|SI, LFA\|SI, SCA\|SI |

### Spain (ES)
| EIC Code | Area Types |
|----------|------------|
| `10YES-REE------0` | BZN\|ES, CTA\|ES, MBA\|ES, LFA\|ES, LFB\|ES, SCA\|ES |

### Sweden (SE)
| EIC Code | Area Types |
|----------|------------|
| `10YSE-1--------K` | CTA\|SE, MBA\|SE, SCA\|SE |
| `10Y1001A1001A44P` | BZN\|SE1, IPA\|SE1, MBA\|SE1, SCA\|SE1 |
| `10Y1001A1001A45N` | BZN\|SE2, IPA\|SE2, MBA\|SE2, SCA\|SE2 |
| `10Y1001A1001A46L` | BZN\|SE3, IPA\|SE3, MBA\|SE3, SCA\|SE3 |
| `10Y1001A1001A47J` | BZN\|SE4, IPA\|SE4, MBA\|SE4, SCA\|SE4 |

### Switzerland (CH)
| EIC Code | Area Types |
|----------|------------|
| `10YCH-SWISSGRIDZ` | BZN\|CH, CTA\|CH, MBA\|CH, LFA\|CH, LFB\|CH, SCA\|CH |

### Turkey (TR)
| EIC Code | Area Types |
|----------|------------|
| `10YTR-TEIAS----W` | BZN\|TR, CTA\|TR, MBA\|TR, LFA\|TR, LFB\|TR, SCA\|TR |

### Ukraine (UA)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001C--00003F` | BZN\|UA, LFB\|UA, MBA\|UA, SCA\|UA |
| `10Y1001C--000182` | BZN\|UA-IPS, CTA\|UA-IPS, LFA\|UA-IPS, MBA\|UA-IPS, SCA\|UA-IPS |
| `10Y1001A1001A869` | BZN\|UA-DobTPP, CTA\|UA-DobTPP, SCA\|UA-DobTPP |
| `10YUA-WEPS-----0` | BZN\|UA-BEI, CTA\|UA-BEI, LFA\|UA-BEI, LFB\|UA-BEI, MBA\|UA-BEI, SCA\|UA-BEI |

### United Kingdom (GB)
| EIC Code | Area Types |
|----------|------------|
| `10Y1001A1001A92E` | United Kingdom (general) |
| `10YGB----------A` | BZN\|GB, CTA\|National Grid, MBA\|GB, LFA\|GB, LFB\|GB, SCA\|GB, SNA\|GB |
| `10Y1001C--00098F` | BZN\|GB(IFA) |
| `11Y0-0000-0265-K` | BZN\|GB(ElecLink) |
| `17Y0000009369493` | BZN\|GB(IFA2) |

---

## 4. EIC Codes by Area Type

### Bidding Zones (BZN) - Most Commonly Used

| Country | EIC Code | Display Name |
|---------|----------|--------------|
| Albania | `10YAL-KESH-----5` | BZN\|AL |
| Austria | `10YAT-APG------L` | BZN\|AT |
| Belgium | `10YBE----------2` | BZN\|BE |
| Bosnia & Herz. | `10YBA-JPCC-----D` | BZN\|BA |
| Bulgaria | `10YCA-BULGARIA-R` | BZN\|BG |
| Croatia | `10YHR-HEP------M` | BZN\|HR |
| Cyprus | `10YCY-1001A0003J` | BZN\|CY |
| Czech Republic | `10YCZ-CEPS-----N` | BZN\|CZ |
| Denmark DK1 | `10YDK-1--------W` | BZN\|DK1 |
| Denmark DK2 | `10YDK-2--------M` | BZN\|DK2 |
| Estonia | `10Y1001A1001A39I` | BZN\|EE |
| Finland | `10YFI-1--------U` | BZN\|FI |
| France | `10YFR-RTE------C` | BZN\|FR |
| Germany-Luxembourg | `10Y1001A1001A82H` | BZN\|DE-LU |
| Greece | `10YGR-HTSO-----Y` | BZN\|GR |
| Hungary | `10YHU-MAVIR----U` | BZN\|HU |
| Ireland (SEM) | `10Y1001A1001A59C` | BZN\|IE(SEM) |
| Italy North | `10Y1001A1001A73I` | BZN\|IT-North |
| Kosovo | `10Y1001C--00100H` | BZN\|XK |
| Latvia | `10YLV-1001A00074` | BZN\|LV |
| Lithuania | `10YLT-1001A0008Q` | BZN\|LT |
| Malta | `10Y1001A1001A93C` | BZN\|MT |
| Moldova | `10Y1001A1001A990` | BZN\|MD |
| Montenegro | `10YCS-CG-TSO---S` | BZN\|ME |
| Netherlands | `10YNL----------L` | BZN\|NL |
| North Macedonia | `10YMK-MEPSO----8` | BZN\|MK |
| Norway NO1 | `10YNO-1--------2` | BZN\|NO1 |
| Norway NO2 | `10YNO-2--------T` | BZN\|NO2 |
| Norway NO3 | `10YNO-3--------J` | BZN\|NO3 |
| Norway NO4 | `10YNO-4--------9` | BZN\|NO4 |
| Norway NO5 | `10Y1001A1001A48H` | BZN\|NO5 |
| Poland | `10YPL-AREA-----S` | BZN\|PL |
| Portugal | `10YPT-REN------W` | BZN\|PT |
| Romania | `10YRO-TEL------P` | BZN\|RO |
| Serbia | `10YCS-SERBIATSOV` | BZN\|RS |
| Slovakia | `10YSK-SEPS-----K` | BZN\|SK |
| Slovenia | `10YSI-ELES-----O` | BZN\|SI |
| Spain | `10YES-REE------0` | BZN\|ES |
| Sweden SE1 | `10Y1001A1001A44P` | BZN\|SE1 |
| Sweden SE2 | `10Y1001A1001A45N` | BZN\|SE2 |
| Sweden SE3 | `10Y1001A1001A46L` | BZN\|SE3 |
| Sweden SE4 | `10Y1001A1001A47J` | BZN\|SE4 |
| Switzerland | `10YCH-SWISSGRIDZ` | BZN\|CH |
| Turkey | `10YTR-TEIAS----W` | BZN\|TR |
| UK | `10YGB----------A` | BZN\|GB |

### Control Areas (CTA)

| Country | EIC Code | Display Name |
|---------|----------|--------------|
| Albania | `10YAL-KESH-----5` | CTA\|AL |
| Austria | `10YAT-APG------L` | CTA\|AT |
| Belgium | `10YBE----------2` | CTA\|BE |
| Bulgaria | `10YCA-BULGARIA-R` | CTA\|BG |
| Czech Republic | `10YCZ-CEPS-----N` | CTA\|CZ |
| Denmark | `10Y1001A1001A796` | CTA\|DK |
| Estonia | `10Y1001A1001A39I` | CTA\|EE |
| Finland | `10YFI-1--------U` | CTA\|FI |
| France | `10YFR-RTE------C` | CTA\|FR |
| Germany (50Hertz) | `10YDE-VE-------2` | CTA\|DE(50Hertz) |
| Germany (Amprion) | `10YDE-RWENET---I` | CTA\|DE(Amprion) |
| Germany (TenneT) | `10YDE-EON------1` | CTA\|DE(TenneT GER) |
| Germany (TransnetBW) | `10YDE-ENBW-----N` | CTA\|DE(TransnetBW) |
| Greece | `10YGR-HTSO-----Y` | CTA\|GR |
| Hungary | `10YHU-MAVIR----U` | CTA\|HU |
| Ireland | `10YIE-1001A00010` | CTA\|IE |
| Italy | `10YIT-GRTN-----B` | CTA\|IT |
| Latvia | `10YLV-1001A00074` | CTA\|LV |
| Lithuania | `10YLT-1001A0008Q` | CTA\|LT |
| Luxembourg | `10YLU-CEGEDEL-NQ` | CTA\|LU |
| Netherlands | `10YNL----------L` | CTA\|NL |
| Norway | `10YNO-0--------C` | CTA\|NO |
| Poland | `10YPL-AREA-----S` | CTA\|PL |
| Portugal | `10YPT-REN------W` | CTA\|PT |
| Romania | `10YRO-TEL------P` | CTA\|RO |
| Serbia | `10YCS-SERBIATSOV` | CTA\|RS |
| Slovakia | `10YSK-SEPS-----K` | CTA\|SK |
| Slovenia | `10YSI-ELES-----O` | CTA\|SI |
| Spain | `10YES-REE------0` | CTA\|ES |
| Sweden | `10YSE-1--------K` | CTA\|SE |
| Switzerland | `10YCH-SWISSGRIDZ` | CTA\|CH |
| UK | `10YGB----------A` | CTA\|National Grid |

---

## 5. Quick Reference Tables

### All Italian Bidding Zones

| EIC Code | Zone Name |
|----------|-----------|
| `10Y1001A1001A73I` | IT-North |
| `10Y1001A1001A70O` | IT-Centre-North |
| `10Y1001A1001A71M` | IT-Centre-South |
| `10Y1001A1001A788` | IT-South |
| `10Y1001A1001A74G` | IT-Sardinia |
| `10Y1001A1001A75E` | IT-Sicily |
| `10Y1001A1001A699` | IT-Brindisi |
| `10Y1001A1001A72K` | IT-Foggia |
| `10Y1001A1001A76C` | IT-Priolo |
| `10Y1001A1001A77A` | IT-Rossano |
| `10Y1001C--00096J` | IT-Calabria |

### All Norwegian Bidding Zones

| EIC Code | Zone Name |
|----------|-----------|
| `10YNO-1--------2` | NO1 (Oslo region) |
| `10Y1001A1001A64J` | NO1A |
| `10YNO-2--------T` | NO2 (Southwest) |
| `10Y1001C--001219` | NO2A |
| `10YNO-3--------J` | NO3 (Central) |
| `10YNO-4--------9` | NO4 (North) |
| `10Y1001A1001A48H` | NO5 (West) |

### All Swedish Bidding Zones

| EIC Code | Zone Name |
|----------|-----------|
| `10Y1001A1001A44P` | SE1 (Luleå) |
| `10Y1001A1001A45N` | SE2 (Sundsvall) |
| `10Y1001A1001A46L` | SE3 (Stockholm) |
| `10Y1001A1001A47J` | SE4 (Malmö) |

### All Danish Bidding Zones

| EIC Code | Zone Name |
|----------|-----------|
| `10YDK-1--------W` | DK1 (West Denmark) |
| `10YDK-1-------AA` | DK1A |
| `10YDK-2--------M` | DK2 (East Denmark) |

### All German TSO Control Areas

| EIC Code | TSO |
|----------|-----|
| `10YDE-VE-------2` | 50Hertz |
| `10YDE-RWENET---I` | Amprion |
| `10YDE-EON------1` | TenneT Germany |
| `10YDE-ENBW-----N` | TransnetBW |

---

## 6. Special Codes and Interconnections

### Regions (REG)

| EIC Code | Region Name |
|----------|-------------|
| `10Y1001A1001A91G` | Nordic |
| `10Y1001C--00031A` | WE_REGION |
| `10Y1001C--00059P` | CORE |
| `10Y1001C--00085O` | MFRR_REGION |
| `10Y1001C--00090V` | AFRR |
| `10Y1001C--00095L` | SWE |
| `10Y1001C--00137V` | ITALYNORTH |
| `10Y1001C--00138T` | GRIT |
| `10YDOM-REGION-1V` | CWE |

### Synchronous Areas (SNA)

| EIC Code | Description |
|----------|-------------|
| `10YEU-CONT-SYNC0` | Continental Europe |
| `10Y1001A1001A91G` | Nordic |
| `10Y1001A1001A59C` | Ireland |
| `10YGB----------A` | GB |

### Load Frequency Control Blocks (LFB)

| EIC Code | Description |
|----------|-------------|
| `10YCB-GERMANY--8` | DE_DK1_LU |
| `10YCB-JIEL-----9` | RS_MK_ME |
| `10YCB-POLAND---Z` | PL |
| `10YCB-SI-HR-BA-3` | SI_HR_BA |
| `10Y1001A1001A91G` | Nordic |

### Bidding Zone Aggregations (BZA)

| EIC Code | Description |
|----------|-------------|
| `10Y1001C--00038X` | CZ-DE-SK-LT-SE4 |
| `10YDOM-1001A082L` | PL-CZ |
| `10YDOM-CZ-DE-SKK` | CZ-DE-SK (BZN\|CZ+DE+SK) |
| `10YDOM-PL-SE-LT2` | LT-SE4 |

### Interconnector Virtual Bidding Zones

| EIC Code | Description |
|----------|-------------|
| `10Y1001C--00098F` | GB(IFA) - Interconnection France-England |
| `11Y0-0000-0265-K` | GB(ElecLink) |
| `17Y0000009369493` | GB(IFA2) |
| `46Y000000000007M` | DK1-NO1 |
| `50Y0JVU59B4JWQCU` | NO2NSL (North Sea Link) |

---

## API Usage Examples

### Example 1: Get Day-Ahead Prices for Germany-Luxembourg

```bash
curl -X GET "https://web-api.tp.entsoe.eu/api" \
  -d "securityToken=YOUR_API_KEY" \
  -d "documentType=A44" \
  -d "in_Domain=10Y1001A1001A82H" \
  -d "out_Domain=10Y1001A1001A82H" \
  -d "periodStart=202401010000" \
  -d "periodEnd=202401020000"
```

### Example 2: Get Load Forecast for France

```bash
curl -X GET "https://web-api.tp.entsoe.eu/api" \
  -d "securityToken=YOUR_API_KEY" \
  -d "documentType=A65" \
  -d "processType=A01" \
  -d "outBiddingZone_Domain=10YFR-RTE------C" \
  -d "periodStart=202401010000" \
  -d "periodEnd=202401020000"
```

### Example 3: Get Cross-Border Flows from Sweden SE3 to Denmark DK1

```bash
curl -X GET "https://web-api.tp.entsoe.eu/api" \
  -d "securityToken=YOUR_API_KEY" \
  -d "documentType=A11" \
  -d "in_Domain=10YDK-1--------W" \
  -d "out_Domain=10Y1001A1001A46L" \
  -d "periodStart=202401010000" \
  -d "periodEnd=202401020000"
```

---

## Notes for API Users

1. **Case Sensitivity**: EIC codes are case-sensitive. Always use the exact format shown.

2. **URL Encoding**: When using EIC codes in URLs, ensure special characters (like `|`) are properly encoded if appearing in display names.

3. **Multiple Area Types**: Many EIC codes serve multiple purposes (BZN, CTA, MBA, etc.). Use the same code regardless of the area type context.

4. **Bidding Zone vs Control Area**: 
   - Use **Bidding Zone (BZN)** codes for market-related queries (prices, volumes)
   - Use **Control Area (CTA)** codes for physical flow and generation queries

5. **Time Zones**: All times in API queries should be in UTC format (YYYYMMDDHHMM).

---

*Document generated from ENTSO-E Transparency Platform documentation. For the most up-to-date information, visit: https://transparency.entsoe.eu/*

