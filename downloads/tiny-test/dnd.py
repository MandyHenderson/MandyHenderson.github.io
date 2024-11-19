import random
import tinytroupe
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson
from tinytroupe.extraction import ResultsExtractor


def create_dnd_character(name, race, character_class, traits, skills, relationships, background, goals):
    """创建一个D&D角色"""
    character = TinyPerson(name)
    character.define("race", race)
    character.define("class", character_class)
    character.define("background", background)
    character.define("goals", goals)
    character.define_several("personality_traits", [{"trait": t} for t in traits])
    character.define_several("skills", [{"skill": s} for s in skills])
    character.define_several("relationships", [{"name": r[0], "description": r[1]} for r in relationships])
    return character


def random_event():
    """生成随机事件"""
    events = [
        {
            "description": "一座摇摇欲坠的吊桥挡住了去路，需要决定谁来修理或跨越。",
            "options": [
                "由Thorin用力量尝试固定吊桥。",
                "由Shade尝试潜行过去并寻找另一条路。",
                "由Elena使用神圣魔法强化桥梁。"
            ]
        },
        {
            "description": "一队哥布林埋伏在前方，你们必须决定战斗还是潜行通过。",
            "options": [
                "直接冲锋，与哥布林正面对战。",
                "由Shade先潜行刺杀领头哥布林，减少敌人数量。",
                "尝试谈判，让哥布林放你们过去。"
            ]
        },
        {
            "description": "地牢中的魔法机关突然启动，导致队伍被分散，需要重新集合。",
            "options": [
                "每人分别寻找安全区域并尝试集合。",
                "使用Elena的神圣感知寻找队友位置。",
                "由Shade利用他的敏捷性去寻找其他人。"
            ]
        },
        {
            "description": "发现了一件宝物，但它似乎被施加了某种诅咒。",
            "options": [
                "由Thorin用战士的意志尝试抵抗诅咒。",
                "由Elena进行神圣净化仪式。",
                "将宝物封存并继续前进。"
            ]
        }
    ]
    return random.choice(events)


def event_resolution(event, world):
    """处理随机事件"""
    description = event["description"]
    options = event["options"]

    print(f"\n==== 随机事件 ====\n")
    print(f"事件描述: {description}\n")
    print("选择: ")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")

    world.broadcast(f"事件发生：{description} 请讨论以下解决方案：{', '.join(options)}")
    world.run(4)


def main():
    """主要冒险场景"""
    # 创建角色
    warrior = create_dnd_character(
        name="Thorin",
        race="Dwarf",
        character_class="Warrior",
        traits=["勇敢", "固执", "忠诚"],
        skills=["斧技精湛", "防御能力强", "团队激励"],
        relationships=[("Elena", "他的队友，一位善良的牧师。"), ("Shade", "不完全信任但尊重的盗贼。")],
        background="一名来自北方山脉的矿工，因保卫家乡而成为战士。",
        goals="寻找传说中的龙之宝石，为家乡赢得荣耀。"
    )

    cleric = create_dnd_character(
        name="Elena",
        race="Elf",
        character_class="Cleric",
        traits=["智慧", "仁慈", "虔诚"],
        skills=["治愈魔法", "神圣打击", "辨别邪恶"],
        relationships=[("Thorin", "她的队友，一个坚定的战士。"), ("Shade", "虽然狡猾但有潜力的盟友。")],
        background="一名神殿的学者，因神的启示加入冒险。",
        goals="摧毁藏在地牢中的古老邪恶力量。"
    )

    rogue = create_dnd_character(
        name="Shade",
        race="Halfling",
        character_class="Rogue",
        traits=["狡猾", "机智", "独立"],
        skills=["潜行", "开锁", "背刺攻击"],
        relationships=[("Thorin", "时而对立但彼此尊重的队友。"), ("Elena", "带有些许怀疑但愿意信任的牧师。")],
        background="曾是一个小偷，因偷窃失败而被迫加入冒险。",
        goals="找到足够的财富来赎回自己家族的遗产。"
    )

    # 创建冒险世界
    world = TinyWorld("Dungeon Adventure", [warrior, cleric, rogue])

    # 初始任务广播
    world.broadcast("""
        各位冒险者，你们面前是一座神秘的地牢，传闻其中藏有传说中的宝藏。
        你们需要合作，解决陷阱与敌人，寻找出口。

        请讨论以下问题：
        1. 谁来担任队长？
        2. 如何应对潜在的危险？
        3. 如果发现宝藏，如何分配？
    """)
    world.run(4)

    # 随机事件处理
    for i in range(3):  # 增加多个事件回合
        event = random_event()
        event_resolution(event, world)

    # 提取结果
    extractor = ResultsExtractor()
    leader = world.get_agent_by_name("Thorin")
    results = extractor.extract_results_from_agent(
        leader,
        extraction_objective="总结团队的讨论结果，包括策略、角色分工和团队互动。",
        situation="冒险队伍进入地牢，面对各种挑战和随机事件的讨论。"
    )

    # 打印总结
    print("\n====== 地牢冒险总结 ======\n")
    print(results)


if __name__ == "__main__":
    main()
