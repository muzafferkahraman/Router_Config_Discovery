# Router_Config_Discovery

This script establishes a Netconf connection towards the SROS Router what support model-driven data model (YANG) and reads the card configs. Then puts all the necessary info to  an excel file.

![](excel_view.JPG)

**cards_library**
This file hosts the dataclasses that map to the router card configs

**discover_cards**
The actual code that fetches the whole router config via the Netconf and then parses the parameters and construct a JSON file.
The JSON then is converted to the excel format, using Pandas module


