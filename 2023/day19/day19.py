""" filesystem paths module """
from pathlib import Path
from copy import deepcopy


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n\n')
        workflows, parts = c
    return (workflows.split('\n'), parts.split('\n'))


class Condition():
    def __init__(self,property, comparison, target) -> None:
        self.property = property
        self.comparison = comparison
        self.target = target

    def __str__(self) -> str:
        return f'{self.property} {self.comparison} {self.target}'


class Rule():
    def __init__(self, conditions, target) -> None:
        self.condition = self.parse_conditions(conditions)
        self.target = target

    def parse_conditions(self, conditions):
        if conditions is not None:
            return Condition(conditions[:1], conditions[1], int(conditions[2:]))
        return Condition(None, None, None)

    def __str__(self) -> str:
        return f'Rule with condition {self.condition} and target {self.target}'


class Part():
    def __init__(self, properties) -> None:
        self.properties = self.parse_properties(properties)

    def parse_properties(self, properties):
        p = {}
        for props in properties.replace('{', '').replace('}', '').split(','):
            split = props.split('=')
            p[split[0]] = int(split[1])
        return p

    def __str__(self) -> str:
        return f'Part with properties {self.properties}'

class Workflow():
    def __init__(self, name: str, rules: list[Rule]) -> None:
        self.name = name
        self.rules: list[Rule] = rules

    def process(self, part: Part):
        for rule in self.rules:
            property = rule.condition.property
            comparison = rule.condition.comparison
            target = rule.condition.target

            if comparison == '>':
                if part.properties[property] > target:
                    return rule.target
            if comparison == '<':
                if part.properties[property] < target:
                    return rule.target
            if comparison is None:
                return rule.target
        raise Exception('No rule applied.')

    def __str__(self) -> str:
        return f'Workflow {self.name} with rules {[x.__str__() for x in self.rules]}'


def solve_workflow_combinations(part, wf_name: str, workflows: dict[str,Workflow], accepted_parts):
    """ Calculate the number of combinations ending in accepting a part """
    wf = workflows[wf_name]
    rule_applied_part = deepcopy(part)
    rule_not_applied_part = deepcopy(part)
    for rule in wf.rules:
        if rule.condition.comparison is not None and rule.condition.target is not None:
            if rule.condition.comparison == '<':
                if rule.condition.target < rule_applied_part[rule.condition.property][1]:
                    rule_applied_part[rule.condition.property][1] = rule.condition.target
                rule_not_applied_part[rule.condition.property][0] = rule.condition.target
            if rule.condition.comparison == '>':
                if rule.condition.target + 1 > rule_applied_part[rule.condition.property][0]:
                    rule_applied_part[rule.condition.property][0] = rule.condition.target + 1
                rule_not_applied_part[rule.condition.property][1] = rule.condition.target + 1

        if rule.target == 'R':
            rule_applied_part = deepcopy(rule_not_applied_part)
            continue
        if rule.target == 'A':
            accepted_parts.append(deepcopy(rule_applied_part))
            rule_applied_part = deepcopy(rule_not_applied_part)
            continue
        solve_workflow_combinations(rule_applied_part, rule.target, workflows, accepted_parts)
        rule_applied_part = deepcopy(rule_not_applied_part) 


if __name__ == '__main__':
    workflows, parts = load_data('input')

    wf: dict[str,Workflow] = {}
    # parse workflows
    for w in workflows:
        split = w.replace('}','').split('{')
        rules = split[1].split(',')
        rs: list[Rule] = []
        for r in rules:
            rule = r.split(':')
            if len(rule) > 1:
                rs.append(Rule(rule[0],rule[1]))
            else:
                rs.append(Rule(None, rule[0]))
        wf[split[0]] = Workflow(split[0],rs)

    # parse parts
    res = 0
    for part in parts:
        workflow = wf['in']
        p = Part(part)
        while True: 
            next_wf_name = workflow.process(p)
            if next_wf_name == 'A' or next_wf_name == 'R':
                if next_wf_name == 'A':
                    res += sum([int(x) for x in p.properties.values()])
                break
            workflow = wf[next_wf_name]

    print('Part one:')
    print(res)

    accepted_parts = []
    solve_workflow_combinations({'x':[1,4001],'m':[1,4001],'a':[1,4001],'s':[1,4001]}, 'in', wf, accepted_parts)
    combos = 0
    for p in accepted_parts:
        res = 1
        for k in p:
            res *= p[k][1]-p[k][0]
        combos += res
    print('Part two:')
    print(combos)
