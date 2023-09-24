import json

class Policy:
    fullAccessList = {
        'oneService': False,
        'fullAdmin': False
    }
    
    def __init__(self, document):
        self.doc = document
        # self.doc = json.loads(document)
        
    ## Only if it is a string objects, some boto3 api does not return as array
    def parseDocumentToJson(self):
        self.doc = json.loads(self.doc)
    
    def inspectAccess(self):
        doc = self.doc
        for statement in doc['Statement']:
            if statement['Effect'] != 'Allow':
                continue
                
            actions = statement['Action']
            actions = actions if isinstance(actions, list) else [actions]
            
            for action in actions:
                perm = action.split(':')
                
                if len(perm) != 1:
                    serv, perm = perm
                else:
                    serv = perm = '*'
                    
                if perm == '*':
                    self.fullAccessList['oneService'] = True
                    
                if perm == '*' and serv == '*':
                    self.fullAccessList['fullAdmin'] = True
                    return
                    
        return False
    
    def hasFullAccessToOneResource(self):
        return self.fullAccessList['oneService']
    
    def hasFullAccessAdmin(self):
        return self.fullAccessList['fullAdmin']
        
    def extractPolicyInfo(self):
        doc = self.doc
        
        policy = {'allow': {}, 'deny': {}}
        for statement in doc['Statement']:
            effect = statement['Effect'].lower()
            policy[effect][statement['Sid']] = {'Principal': statement['Principal'], 'Action': statement['Action']}
            
        return policy