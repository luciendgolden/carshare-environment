from fuzzylogic.classes import Domain, Rule

class FIS:
    """Represents Fuzzy Inference System
    
    Attributes:
        domains     A list of domains (input and output variables)
        rules       A dictionary. Keys are domain names, values are tuples. Tuple contains a list of inputs and a fuzzylogic.classes.Rule object
                    Example:
                    self.rules["gas_station"] = (["fuel", "ride_time"], gas_station_rules)
    """
    def __init__(self):
        self.domains = []
        self.rules = {}
    
    def add_rule(self, domain_name: str, input_list: list[str], rule: Rule) -> dict[str, tuple[list[str]], Rule]:
        """Add a rule"""
        self.rules[domain_name] = (input_list, rule)
        print(f"Rules for {domain_name} were added")
        #print(self.rules)
        return self.rules
    
    def add_domain(self, domain: Domain) -> list[Domain]:
        """Add a domain"""
        print(f'Domain {domain} was added')
        return self.domains.append(domain)

    # Used as decorator
    def domain(self, define_domain):
        # call the define_domain function, add the result to domain list
        self.add_domain(define_domain())
        return define_domain
    
    # Used as decorator
    def rule(self, get_rules):
        # call the get_rules function, add the result to rules list
        result = get_rules()
        self.add_rule(result[0], result[1], result[2])
        return get_rules

# create a fis
fis = FIS()