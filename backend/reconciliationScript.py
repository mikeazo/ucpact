#!/usr/bin/env python

# import os
import json
from pathlib import Path

def convert_files(filenames: list[Path]):
    for fileName in filenames:
        with open(fileName, 'r') as fp:
            full_data = json.load(fp)
        if 'modelVersion' in full_data and full_data['modelVersion'] == '1.3':
            # skip this model
            continue
        if 'modelVersion' in full_data and full_data['modelVersion'] == '1.2':
            # add blank comments to json
            add_comment_to_messages(full_data)
            add_comment_to_basic_interfaces(full_data)
            add_comment_to_comp_interfaces(full_data)
            add_comment_to_parties(full_data)
            add_comment_to_states(full_data)
            # Change model version
            full_data['modelVersion'] = '1.3'
            full_data['model']['modelVersion'] = '1.3'

            with open(fileName, 'w') as fp:
                json.dump(full_data, fp, indent=2)

                print(fileName.stem + " updated")
            # then skip
            continue
        # Update parameter interface object
        if 'modelVersion' not in full_data or full_data['modelVersion'] != '1.1':
            paramInters = full_data['model']['realFunctionality']['parameterInterfaces']
            for paramInter in paramInters:
                paramInter['left'] = ''
                paramInter['top'] = ''
                paramInter['color'] = '#de8989'

        # add blank comments to json
        add_comment_to_messages(full_data)
        add_comment_to_basic_interfaces(full_data)
        add_comment_to_comp_interfaces(full_data)
        add_comment_to_parties(full_data)
        add_comment_to_states(full_data)

        # Update transitions
        transitions = full_data['model']['stateMachines']['transitions']

        # Add transition name
        for transition in transitions:
            if 'name' not in transition:
                transition['name'] = ''

        stateMachines = full_data['model']['stateMachines']['stateMachines']
        for stateMachine in stateMachines:
            stateMachineTransitionsId = stateMachine['transitions']
            stateMachineTransitions = []
            for transitionA in stateMachineTransitionsId:
                for transitionB in transitions:
                    if transitionA == transitionB['id']:
                        stateMachineTransitions.append(transitionB)

            # Add transition handles
            count = 0
            for transitionA in stateMachineTransitions:
                for transitionB in stateMachineTransitions:
                    if (transitionA['fromState'] == transitionB['fromState']) and (transitionA['toState'] == transitionB['toState']):
                        if 'sourceHandle' not in transitionA:
                            sourceHandle = 13 - count
                            transitionA['sourceHandle'] = str(sourceHandle)

                        if 'targetHandle' not in transitionA:
                            targetHandle = 1 + count
                            transitionA['targetHandle'] = str(targetHandle)

                        count += 1
                    else:
                        transitionA['sourceHandle'] = '13'
                        transitionA['targetHandle'] = '1'

        # Update state positioning
        states = full_data['model']['stateMachines']['states']
        for state in states:
            state['left'] = state['left'] - 245
            state['top'] = state['top'] - 100
        
        # Change model version
        full_data['modelVersion'] = '1.3'
        full_data['model']['modelVersion'] = '1.3'

        with open(fileName, 'w') as fp:
            json.dump(full_data, fp, indent=2)

            print(fileName.stem + " updated")

# helper functions
def add_comment_to_messages(data):

    updated_messages = []
    for msg in data['model']['interfaces']['messages']:
        if "messageComment" not in msg:
            new_msg = msg.copy()
            for key in msg:
                new_msg[key] = msg[key]
                if 'id' in msg:
                    new_msg["messageComment"] = ""
            msg = new_msg
        updated_messages.append(msg)

    data['model']['interfaces']["messages"] = updated_messages

def add_comment_to_comp_interfaces(data):
    updated_comps = []
    for compInter in data['model']['interfaces']['compInters']:
        if "interfaceComment" not in compInter:
            new_comp = compInter.copy()
            for key in compInter:
                new_comp[key] = compInter[key]
                if key == "id":
                    new_comp["interfaceComment"] = ""
            compInter = new_comp
        updated_comps.append(compInter)

    data['model']['interfaces']["compInters"] = updated_comps

def add_comment_to_basic_interfaces(data):
    updated_basics = []
    for basicInter in data['model']['interfaces']['basicInters']:
        if "interfaceComment" not in basicInter:
            new_basic = basicInter.copy()
            for key in basicInter:
                new_basic[key] = basicInter[key]
                if key == "id":
                    new_basic["interfaceComment"] = ""
            basicInter = new_basic
        updated_basics.append(basicInter)

    data['model']['interfaces']["basicInters"] = updated_basics

def add_comment_to_parties(data):
    updated_parties = []
    for party in data['model']['parties']['parties']:
        if "comment" not in party:
            new_party = party.copy()
            for key in party:
                new_party[key] = party[key]
                if key == "id":
                    new_party["comment"] = ""
            party = new_party
        updated_parties.append(party)

    data['model']['parties']["parties"] = updated_parties

def add_comment_to_states(data):
    updated_states = []
    for state in data['model']['stateMachines']['states']:
        if "comment" not in state:
            new_state = state.copy()
            for key in state:
                new_state[key] = state[key]
                if key == "id":
                    new_state["comment"] = ""
            state = new_state
        updated_states.append(state)

    data['model']['stateMachines']["states"] = updated_states


# main
if __name__ == "__main__":
    model_folder = Path('./models')
    filenames = [
        filepath for filepath in model_folder.iterdir()
        if filepath.suffix == '.json'
    ]
    convert_files(filenames)