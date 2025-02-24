import pandas as pd
import numpy as np
import random
from collections import deque
from scipy.stats import beta
results = []
k1=0
k2=0
k3=0
def calculate_profit(scenario, decisions, iterations=20):
    components = scenario['components']
    semi_products = scenario['semi_products']
    final_product = scenario['final_product']

    inspect_components, inspect_semi, inspect_final, disassemble_semi, disassemble_final = decisions
    kt=0
    total_profit = 0
    components_in_circulation = {i: 1 for i in range(1, 9)}  # 初始时每种零件都有1个
    semi_products_in_circulation = {1: 0, 2: 0, 3: 0}  # 初始时每种半成品都有1个

    for k in range(iterations):

        # 计算零件的期望成本和合格率
        component_costs = {}
        component_good_rates = {}
        for i, (defect_rate, price, inspect_cost) in components.items():
            if k==0:
                component_costs[i] = (price + (inspect_components[i - 1] * inspect_cost))/(1-inspect_components[i - 1]*0.1)


            else:
                component_costs[i] = 0
            if inspect_components[i - 1]:
                 component_good_rates[i] = 1
            else:
                  component_good_rates[i] = 1 - defect_rate

            # 计算半成品的期望成本和合格率
        semi_costs = {}
        semi_good_rates = {}
        for i, (defect_rate, assemble_cost, inspect_cost) in semi_products.items():
            if i == 1:
                components_used = [1, 2, 3]
            elif i == 2:
                components_used = [4, 5, 6]
            else:  # i == 3
                components_used = [7, 8]

            component_good_rate = np.prod([component_good_rates[j] for j in components_used])


            if inspect_semi[i-1]:
                semi_good_rates[i]=  1
            else:
                semi_good_rates[i] = component_good_rate* (1 - 0.1)


            if k==0:
                semi_costs={1:component_costs[1]+component_costs[2]+component_costs[3]+8,2:  component_costs[4] + component_costs[5] + component_costs[6]+8,3: component_costs[7] + component_costs[8]+8}


                if i==1:
                 k1=component_good_rate


                elif i==2:
                 k2=component_good_rate

                else :
                 k3= component_good_rate
                 semi_costs = {1: (component_costs[1] + component_costs[2] + component_costs[3] + 8 + inspect_semi[0] * inspect_cost) / (1 - inspect_semi[0] *(1-0.9*k1) ),
                              2: (component_costs[4] + component_costs[5] + component_costs[6] + 8 + inspect_semi[ 1] * inspect_cost) / (1 - inspect_semi[1]  * (1-0.9*k2)),
                              3: (component_costs[7] + component_costs[8] + 8 + inspect_semi[2] * inspect_cost) / (1 - inspect_semi[2]  * (1-0.9*k3))}








            else:
             semi_costs[i]=((assemble_cost+(inspect_semi[i - 1] * inspect_cost))*(disassemble_semi[i - 1]))*(semi_products_in_circulation[i])



            # 计算最终产品的期望成本和合格率
        final_defect_rate, final_assemble_cost, final_inspect_cost, final_price, replace_cost, disassemble_cost = final_product
        final_cost = sum(semi_costs.values()) + final_assemble_cost
        final_cost += inspect_final * final_inspect_cost #+概率

        semi_good_rate = np.prod(list(semi_good_rates.values()))

        if inspect_final:
            final_good_rate = 1
        else:
            final_good_rate = (1 - final_defect_rate) * semi_good_rate



        # 计算收益
        if k==0:
            revenue = final_price * (1 - final_defect_rate) * semi_good_rate



        else:
            revenue = final_price * (1 - final_defect_rate) * semi_good_rate * min(semi_products_in_circulation.values())



        cost = final_cost

        if not inspect_final:
            cost+= replace_cost * (1 - final_good_rate)

            # 处理拆解
        if disassemble_final:
            disassembled_final = (1 -(1 - final_defect_rate) * semi_good_rate )
            cost += disassemble_cost * disassembled_final
            for i in range(1, 4):
                if k==0:
                 semi_products_in_circulation[i] = disassembled_final#前面检测不合格的可以加到这

                else:
                 semi_products_in_circulation[i] = disassembled_final*semi_products_in_circulation[i]



        else:
            for i in range(1, 4):

                semi_products_in_circulation[i] = 0#与上面同一问题

        for i, disassemble in enumerate(disassemble_semi, 1):
            if disassemble:
                if k==0:
                 disassembled_semi = (1 - semi_good_rates[i])
                else:
                 disassembled_semi= (1 - semi_good_rates[i])*semi_products_in_circulation[i]
                cost += semi_products[i][2] * disassembled_semi  # 使用检测成本作为拆解成本
                if i == 1:
                    for j in range(1, 4):
                        components_in_circulation[j] = disassembled_semi
                elif i == 2:
                    for j in range(4, 7):
                        components_in_circulation[j] = disassembled_semi
                else:  # i == 3
                    for j in range(7, 9):
                        components_in_circulation[j] = disassembled_semi
            else:
                if i == 1:
                    for j in range(1, 4):
                        components_in_circulation[j] = 0
                elif i == 2:
                    for j in range(4, 7):
                        components_in_circulation[j] = 0
                else:  # i == 3
                    for j in range(7, 9):
                        components_in_circulation[j] = 0

        iteration_profit = revenue - cost

        if iteration_profit<0:
            break

        total_profit += iteration_profit
        kt+=cost


        if all(v < 0.01 for v in components_in_circulation.values()) and all(
                v < 0.01 for v in semi_products_in_circulation.values()):
            break
    for j in range(1, 9):
        total_profit += components_in_circulation[j] * inspect_components[j - 1] * component_costs[j]
        kt-= components_in_circulation[j] * inspect_components[j - 1] * component_costs[j]
    if kt == 0:
        jjj = 0
    else:
        jjj = total_profit / kt
    return jjj



def improved_genetic_algorithm(scenario, population_size=100, generations=500, elite_size=10, local_search_prob=0.1):
    def create_individual():
        return (
            tuple(random.choice([True, False]) for _ in range(8)),  # inspect_comp
            tuple(random.choice([True, False]) for _ in range(3)),  # inspect_semi
            random.choice([True, False]),  # inspect_final
            tuple(random.choice([True, False]) for _ in range(3)),  # disassemble_semi
            random.choice([True, False])  # disassemble_final
        )

    def crossover(parent1, parent2):
        child = []
        for p1, p2 in zip(parent1, parent2):
            if isinstance(p1, tuple):
                split = random.randint(0, len(p1))
                child.append(p1[:split] + p2[split:])
            else:
                child.append(random.choice([p1, p2]))
        return tuple(child)

    def mutate(individual, mutation_rate):
        mutated = list(individual)
        for i, gene in enumerate(individual):
            if isinstance(gene, tuple):
                mutated[i] = tuple(not g if random.random() < mutation_rate else g for g in gene)
            else:
                if random.random() < mutation_rate:
                    mutated[i] = not gene
        return tuple(mutated)

    def local_search(individual):
        best_individual = individual
        best_fitness = calculate_profit(scenario, individual)

        for i in range(len(individual)):
            if isinstance(individual[i], tuple):
                for j in range(len(individual[i])):
                    neighbor = list(individual)
                    neighbor[i] = list(neighbor[i])
                    neighbor[i][j] = not neighbor[i][j]
                    neighbor[i] = tuple(neighbor[i])
                    neighbor = tuple(neighbor)

                    fitness = calculate_profit(scenario, neighbor)
                    if fitness > best_fitness:
                        best_individual = neighbor
                        best_fitness = fitness
            else:
                neighbor = list(individual)
                neighbor[i] = not neighbor[i]
                neighbor = tuple(neighbor)

                fitness = calculate_profit(scenario, neighbor)
                if fitness > best_fitness:
                    best_individual = neighbor
                    best_fitness = fitness

        return best_individual

    population = [create_individual() for _ in range(population_size)]
    best_solution = None
    best_fitness = float('-inf')
    stagnation_counter = 0
    fitness_history = deque(maxlen=50)
    mutation_rate = 0.1
    generation_best_decisions = []  # 用于存储每一代的最佳决策

    for generation in range(generations):
        fitness_scores = [calculate_profit(scenario, individual) for individual in population]

        current_best = max(fitness_scores)
        current_best_index = fitness_scores.index(current_best)
        current_best_decision = population[current_best_index]

        generation_best_decisions.append((generation, current_best_decision, current_best))

        print(f"Generation {generation}: Max fitness = {current_best}, Min fitness = {min(fitness_scores)}")

        if current_best > best_fitness:
            best_fitness = current_best
            best_solution = current_best_decision
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if len(fitness_history) == 50:
            if np.mean(list(fitness_history)[-10:]) > np.mean(list(fitness_history)[:10]):
                mutation_rate = max(0.01, mutation_rate * 0.9)
            else:
                mutation_rate = min(0.5, mutation_rate * 1.1)

        fitness_history.append(current_best)

        elite = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)[:elite_size]
        elite = [e[0] for e in elite]

        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            print("Warning: All individuals have zero fitness. Restarting population.")
            population = [create_individual() for _ in range(population_size)]
            continue

        selection_probs = [f / total_fitness for f in fitness_scores]
        new_population = elite

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, weights=selection_probs, k=2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)

            if random.random() < local_search_prob:
                child = local_search(child)

            new_population.append(child)

        population = new_population

        if stagnation_counter >= 50:
            print("Stagnation detected. Restarting population.")
            population = [create_individual() for _ in range(population_size)]
            population[:elite_size] = elite
            stagnation_counter = 0

    if best_solution is None:
        print("Warning: No valid solution found. Returning random individual.")
        return create_individual(), generation_best_decisions

    return best_solution, generation_best_decisions

def find_best_decision_with_improved_ga(scenario):
    best_decision, generation_best_decisions = improved_genetic_algorithm(scenario)
    best_profit = calculate_profit(scenario, best_decision)
    return best_decision, best_profit, generation_best_decisions
for l in range(1,100):
 m11=1.6
 n11=11
 k1=beta.rvs(m11, n11)
 k2=beta.rvs(m11, n11)
 k3=beta.rvs(m11, n11)
 k4=beta.rvs(m11, n11)
 k5=beta.rvs(m11, n11)
 k6=beta.rvs(m11, n11)
 k7=beta.rvs(m11, n11)
 k8=beta.rvs(m11, n11)
 k9=beta.rvs(m11, n11)
 k10=beta.rvs(m11, n11)
 k11=beta.rvs(m11, n11)
 k12=beta.rvs(m11, n11)




# 主程序
 scenario = {
     'components': {
         1: (eval('k1'), 2, 1),
         2: (eval('k2'), 8, 1),
         3: (eval('k3'), 12, 2),
         4: (eval('k4'), 2, 1),
         5: (eval('k5'), 8, 1),
         6: (eval('k6'), 12, 2),
         7: (eval('k7'), 8, 1),
         8: (eval('k8'), 12, 2)
    },
     'semi_products': {
         1: (eval('k9'), 8, 4),
         2: (eval('k10'), 8, 4),
         3: (eval('k11'), 8, 4)
    },
     'final_product': (eval('k12'), 8, 6, 200, 40, 10)
}

 best_decision, best_profit, generation_best_decisions = find_best_decision_with_improved_ga(scenario)
 results.append({

     "检测零件": best_decision[0],
     "检测半成品": best_decision[1],
     "检测最终产品": best_decision[2],
     "拆解半成品": best_decision[3],
     "拆解最终产品": best_decision[4],
     "预期利润": best_profit
 })


print("\n每代最佳决策:")
for gen, decision, fitness in generation_best_decisions:
    if gen % 5 == 0:  # 每10代输出一次，以避免输出过多

        print(f"\n第 {gen} 代最佳决策:")
        print(f"  检测零件: {decision[0]}")
        print(f"  检测半成品: {decision[1]}")
        print(f"  检测最终产品: {decision[2]}")
        print(f"  拆解半成品: {decision[3]}")
        print(f"  拆解最终产品: {decision[4]}")
        print(f"  预期利润: {fitness:.2f}")
df = pd.DataFrame(results)

# 将DataFrame保存为Excel文件
excel_filename = "optimization_results999.xlsx"
df.to_excel(excel_filename, index=False)
print(f"结果已保存到 {excel_filename}")