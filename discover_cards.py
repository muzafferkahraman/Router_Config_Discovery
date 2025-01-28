import copy
from ncclient import manager
import xmltodict
from dataclasses import dataclass
import json
import pandas as pd
from cards_library import *
                                                                                        
def append_to_discovered(discovered_array,snippet):
    snippet_as_dictionary = snippet.__dict__
    cleaned_snippet={k: v for k, v in snippet_as_dictionary.items() if v != None}
    discovered_array.append(cleaned_snippet)

def place_in_array(data):
  if isinstance(data, dict):
    return [data]
  if data==None:
    return []
  else:
    return data

def discover_cards(config)-> None:

    cards=[]

    Discovery=[]
    
    data=config.get("card", None)
    
    if data:
        mdata=place_in_array(data)
        for nugget in mdata:
                json_snippet=Card(
                    context="card",
                    card_id=nugget.get("slot-number"),
                    card_mda_type=nugget.get("card-type"),
                    admin_state=nugget.get("admin-state"))
                append_to_discovered(Discovery,json_snippet)

                if nugget.get("mda", None):
                    for item in place_in_array(nugget.get("mda", {})):
                        json_snippet=Mda(
                            context="mda",
                            card_id=nugget.get("slot-number"),
                            subcard_id=nugget.get("mda-slot"),
                            card_mda_type=item.get("mda-type"),
                            xiom_id=item.get("xiom-id"),
                            admin_state=item.get("admin-state"))     
                        append_to_discovered(Discovery,json_snippet)

                if nugget.get("xiom", None):
                    for item in place_in_array(nugget.get("xiom", {})):
                        json_snippet=Xiom(
                            context="xiom",
                            card_id=nugget.get("slot-number"),
                            xiom_id=item.get("xiom-slot"),
                            card_mda_type=item.get("xiom-type"),
                            admin_state=item.get("admin-state"))     
                        append_to_discovered(Discovery,json_snippet)
                
                if nugget.get("fp", None):
                    for item in place_in_array(nugget["fp"]):
                        json_snippet=Fp(
                            context="fp",
                                card_id=nugget.get("slot-number"),
                                subcard_id=nugget.get("fp-number"),
                                ingress_network_slope_policy=item.get("ingress",{}).get("network",{}).get("pool",{}).get("slope-policy", None),
                                ingress_network_queue_policy=item.get("ingress",{}).get("network",{}).get("queue-policy", None),
                                fp_dist_cpu_dynamic_policer_pool=item.get("ingress",{}).get("dist-cpu-protection",{}).get("dynamic-enforcement-policer-pool", None),
                                admin_state=item.get("admin-state"))  
                        append_to_discovered(Discovery,json_snippet)
       
    data=config.get("sfm", None)
    if data:
        mdata=place_in_array(data)
        for nugget in mdata:
                json_snippet=Sfm(
                    context="sfm",
                    card_id=nugget.get("sfm-slot"),
                    card_mda_type=nugget.get("sfm-type"),
                    admin_state=nugget.get("admin-state"))
                append_to_discovered(Discovery,json_snippet)

    if Discovery != []:
        cards.extend(Discovery)

    cards=json.dumps(cards)
    return  cards

if __name__=="__main__": 
   
    ncc_connection_p = {"host": <ip here>,"port":830,"username":"admin","password":<password here>,"hostkey_verify":False,"allow_agent":False, "timeout": 300} 
    session = manager.connect(**ncc_connection_p)
    xml_content = session.get()
    
    refined_xml_content=xml_content.data_xml  
    json_content = xmltodict.parse( refined_xml_content)   

    config = copy.deepcopy(json_content['data']['configure']) 

    if type(config)==list:   
        configs=config[1]
    else:
        configs=config
    cards_data = json.loads(discover_cards(configs))
        
    df=pd.DataFrame(cards_data)
    df.to_excel("cards.xlsx", index=False)












