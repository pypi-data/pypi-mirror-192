from typing import no_type_check

import pytest

from hyperborea3.chargen import (
    ac_to_aac,
    apply_spells_per_day_bonus,
    calculate_ac,
    class_id_to_name,
    get_age,
    get_alignment,
    get_attr,
    get_attr_mod,
    get_caster_schools,
    get_class_abilities,
    get_class_id_map,
    get_class_level_data,
    get_class_requirements,
    get_combat_matrix,
    get_complexion,
    get_deity,
    get_eye_colour,
    get_favoured_weapons,
    get_gender,
    get_hair_colour,
    get_hd,
    get_height_and_weight,
    get_height_weight_lookup_vals,
    get_languages,
    get_level,
    get_next_atk_rate,
    get_priest_abilities,
    get_qualifying_classes,
    get_race,
    get_race_id,
    get_random_familiar,
    get_random_spell,
    get_save_bonuses,
    get_secondary_skill,
    get_spells,
    get_starting_armour,
    get_starting_gear,
    get_starting_money,
    get_starting_shield,
    get_starting_weapons_melee,
    get_starting_weapons_missile,
    get_thief_skills,
    get_turn_undead_matrix,
    get_unskilled_weapon_penalty,
    get_xp_bonus,
    get_xp_to_next,
    inches_to_feet,
    roll_hit_points,
    roll_stats,
    select_random_class,
)
from hyperborea3.valid_data import (
    VALID_ABILITY_SCORES,
    VALID_ABILITIES,
    VALID_ALIGMENTS_SHORT,
    VALID_CA,
    VALID_CLASS_ID_MAP,
    VALID_CLASS_IDS,
    VALID_CLASS_THIEF_ABILITIES,
    VALID_COMPLEXIONS,
    VALID_DEITIES,
    VALID_DEITY_IDS,
    VALID_DENOMINATIONS,
    VALID_DICE_METHODS,
    VALID_EYE_COLOURS,
    VALID_FA,
    VALID_FAMILIARS,
    VALID_FAVOURED_WEAPONS,
    VALID_GENDERS,
    VALID_GP,
    VALID_HAIR_COLOURS,
    VALID_HD_PLUS,
    VALID_HD_QTY,
    VALID_HD_SIZE,
    VALID_LEVELS,
    VALID_RACE_IDS,
    VALID_RACES_BY_ID,
    VALID_SAVES,
    VALID_SECONDARY_SKILLS,
    VALID_SCHOOLS,
    VALID_SCHOOLS_BY_CLASS_ID,
    VALID_SPELL_LEVELS,
    VALID_TA,
    VALID_UNSKILLED_PENALTIES,
)


@no_type_check
def test_apply_spells_per_day_bonus():
    # test for empty spells
    spells = apply_spells_per_day_bonus(None, bonus_spells_in=4, bonus_spells_ws=4)
    assert spells is None

    # test for magician
    spells = get_spells(class_id=2, level=1, ca=1)
    assert spells["mag"]["spells_per_day"]["lvl1"] == 1
    assert spells["mag"]["spells_per_day"]["lvl2"] == 0
    assert spells["mag"]["spells_per_day"]["lvl3"] == 0
    assert spells["mag"]["spells_per_day"]["lvl4"] == 0
    assert spells["mag"]["spells_per_day"]["lvl5"] == 0
    assert spells["mag"]["spells_per_day"]["lvl6"] == 0
    updated_spells = apply_spells_per_day_bonus(
        spells,
        bonus_spells_in=4,
        bonus_spells_ws=0,
    )
    assert updated_spells["mag"]["spells_per_day"]["lvl1"] == 2
    assert updated_spells["mag"]["spells_per_day"]["lvl2"] == 0
    assert updated_spells["mag"]["spells_per_day"]["lvl3"] == 0
    assert updated_spells["mag"]["spells_per_day"]["lvl4"] == 0
    assert updated_spells["mag"]["spells_per_day"]["lvl5"] == 0
    assert updated_spells["mag"]["spells_per_day"]["lvl6"] == 0

    # test for cleric
    spells = get_spells(class_id=3, level=1, ca=1)
    assert spells["clr"]["spells_per_day"]["lvl1"] == 1
    assert spells["clr"]["spells_per_day"]["lvl2"] == 0
    assert spells["clr"]["spells_per_day"]["lvl3"] == 0
    assert spells["clr"]["spells_per_day"]["lvl4"] == 0
    assert spells["clr"]["spells_per_day"]["lvl5"] == 0
    assert spells["clr"]["spells_per_day"]["lvl6"] == 0
    updated_spells = apply_spells_per_day_bonus(
        spells,
        bonus_spells_in=0,
        bonus_spells_ws=4,
    )
    assert updated_spells["clr"]["spells_per_day"]["lvl1"] == 2
    assert updated_spells["clr"]["spells_per_day"]["lvl2"] == 0
    assert updated_spells["clr"]["spells_per_day"]["lvl3"] == 0
    assert updated_spells["clr"]["spells_per_day"]["lvl4"] == 0
    assert updated_spells["clr"]["spells_per_day"]["lvl5"] == 0
    assert updated_spells["clr"]["spells_per_day"]["lvl6"] == 0

    # test for runegraver
    spells = get_spells(class_id=20, level=1, ca=1)
    updated_spells = apply_spells_per_day_bonus(spells, 4, 4)
    assert spells == updated_spells


@pytest.mark.repeat(10)
def test_get_age():
    for race_id in VALID_RACE_IDS:
        age = get_age(race_id)
        assert isinstance(age, int)
        if race_id == 5:
            assert 14 <= age <= 100
        else:
            assert 14 <= age <= 44


def test_get_xp_bonus():
    class_id = 1
    attr = {"st": {"score": 16}}
    assert get_xp_bonus(class_id, attr) is True
    attr = {"st": {"score": 15}}
    assert get_xp_bonus(class_id, attr) is False


def test_get_xp_to_next():
    for class_id in VALID_CLASS_IDS:
        for level in VALID_LEVELS:
            xp_to_next = get_xp_to_next(class_id, level)
            if level == 12:
                assert xp_to_next is None
            else:
                assert isinstance(xp_to_next, int)
                assert 0 < xp_to_next <= 960_000


def test_roll_stats():
    for class_id in VALID_CLASS_IDS:
        for i in range(100):
            attr = roll_stats(method=6, class_id=class_id)
            for stat in attr.keys():
                assert stat in VALID_ABILITIES
                assert attr[stat]["score"] in VALID_ABILITY_SCORES
    for method in VALID_DICE_METHODS[:5]:
        for i in range(1000):
            attr = roll_stats(method=method)
            for stat in attr.keys():
                assert stat in VALID_ABILITIES
                assert attr[stat]["score"] in VALID_ABILITY_SCORES
    # selecting method 6 without a specific class_id should raise an exception
    with pytest.raises(ValueError):
        attr = roll_stats(method=6)
    # valid methods are 1-6, so a value outside that should raise an exception
    with pytest.raises(ValueError):
        attr = roll_stats(method=7)


def test_get_class_abilities():
    for class_id in VALID_CLASS_IDS:
        for level in VALID_LEVELS:
            class_abilities = get_class_abilities(class_id, level)
            assert isinstance(class_abilities, list)
            assert all([isinstance(x, dict) for x in class_abilities])
            assert all([x["level"] <= level for x in class_abilities])
            assert all([isinstance(x["ability_title"], str) for x in class_abilities])
            # Not populated yet
            # assert all([isinstance(x["ability_desc"], str) for x in class_abilities])


def test_get_class_id_map():
    class_id_map = get_class_id_map()
    assert class_id_map == VALID_CLASS_ID_MAP


@pytest.mark.parametrize(
    "class_id,expected",
    [(k, v) for k, v in VALID_CLASS_ID_MAP.items()],
)
def test_class_id_to_name(class_id: int, expected: str) -> None:
    class_name = class_id_to_name(class_id)
    assert class_name == expected


def test_get_attr_mod():
    actual = get_attr_mod(stat="st", score=18)
    expected = {
        "score": 18,
        "atk_mod": 2,
        "dmg_adj": 3,
        "test": 5,
        "feat": 32,
    }
    assert actual == expected
    with pytest.raises(ValueError):
        get_attr_mod(stat="FakeStat", score=10)


def test_get_priest_abilities():
    for deity_id in VALID_DEITY_IDS:
        for level in [1, 9]:
            priest_abilities = get_priest_abilities(deity_id, level)
            if level >= 9:
                assert len(priest_abilities) == 2
            else:
                assert len(priest_abilities) == 1


@pytest.mark.repeat(1000)
def test_get_qualifying_classes():
    subclasses = 2
    attr = get_attr()
    qual_classes = get_qualifying_classes(attr, subclasses)
    assert all([c in VALID_CLASS_IDS for c in qual_classes])

    subclasses = 1
    attr = get_attr()
    qual_classes = get_qualifying_classes(attr, subclasses)
    assert all([c in range(1, 27) for c in qual_classes])

    subclasses = 0
    attr = get_attr()
    qual_classes = get_qualifying_classes(attr, subclasses)
    assert all([c in range(1, 5) for c in qual_classes])


def test_get_qualifying_classes_invalid():
    # invalid value for subclasses should raise an exception
    attr = get_attr()
    with pytest.raises(ValueError):
        get_qualifying_classes(attr, subclasses=3)


def test_get_level():
    # TODO: Rework this slow af test
    for class_id in VALID_CLASS_IDS:
        for xp in range(0, 1000000, 1000):
            level = get_level(class_id, xp)
            assert level in VALID_LEVELS


def test_get_next_atk_rate():
    atk_progression = [
        "1/1",
        "3/2",
        "2/1",
        "5/2",
        "3/1",
    ]
    for atk_rate in atk_progression[:-1]:
        next_atk_rate = get_next_atk_rate(atk_rate)
        assert next_atk_rate in atk_progression
    with pytest.raises(ValueError):
        get_next_atk_rate(atk_progression[-1])


def test_get_race_id():
    for i in range(1000):
        race_id = get_race_id()
        assert race_id in VALID_RACE_IDS


def test_get_race():
    for race_id in VALID_RACE_IDS:
        race = get_race(race_id)
        assert isinstance(race, str)
        assert race in VALID_RACES_BY_ID.values()


def test_get_gender():
    for i in range(1000):
        gender = get_gender()
        assert gender in VALID_GENDERS


def test_get_save_bonuses():
    for class_id in VALID_CLASS_IDS:
        sv_bonus = get_save_bonuses(class_id)
        for k, v in sv_bonus.items():
            assert v in [0, 2]
        # barbarians, berserkers, and paladins get +2 to all saves
        if class_id in [5, 6, 9, 27]:
            assert sum([v for v in sv_bonus.values()]) == 10
        # all others get +2 to two saves
        else:
            assert sum([v for v in sv_bonus.values()]) == 4


def test_get_class_level_data():
    for class_id in VALID_CLASS_IDS:
        for level in VALID_LEVELS:
            cl_data = get_class_level_data(class_id, level)
            assert cl_data["fa"] in VALID_FA
            assert cl_data["ca"] in VALID_CA
            assert cl_data["ta"] in VALID_TA
            assert cl_data["sv"] in VALID_SAVES


def test_get_class_requirements():
    actual = get_class_requirements(class_id=5)
    actual.sort(key=lambda x: x["attr"])
    expected = [
        {"class_id": 5, "attr": "cn", "min_score": 13},
        {"class_id": 5, "attr": "dx", "min_score": 13},
        {"class_id": 5, "attr": "st", "min_score": 13},
    ]
    assert actual == expected


def test_get_hd():
    for class_id in VALID_CLASS_IDS:
        for level in VALID_LEVELS:
            hd = get_hd(class_id, level)
            qty = hd.split("d")[0]
            # number of dice in 1-9
            assert int(qty) in VALID_HD_QTY
            part2 = hd.split("d")[1].split("+")
            assert len(part2) in [1, 2]
            # die size in d4, d6, d8, d10, d12
            assert int(part2[0]) in VALID_HD_SIZE
            if len(part2) == 2:
                # +hp in 1,2,3; 2,4,6; 3,6,9; 4,8,12
                assert int(part2[1]) in VALID_HD_PLUS


def test_roll_hit_points():
    max_possible_hp = (10 * 12) + (12 * 3)  # Barbarian
    for class_id in VALID_CLASS_IDS:
        for level in VALID_LEVELS:
            for cn_score in VALID_ABILITY_SCORES:
                mods = get_attr_mod("cn", cn_score)
                hp_adj = mods["hp_adj"]
                hp = roll_hit_points(class_id, level, hp_adj)
                assert level <= hp <= max_possible_hp


def test_get_combat_matrix():
    for fa in VALID_FA:
        combat_matrix = get_combat_matrix(fa)
        assert list(combat_matrix.keys()) == list(range(-9, 10))
        assert combat_matrix[0] == 20 - fa


def test_starting_armour():
    for class_id in VALID_CLASS_IDS:
        armour = get_starting_armour(class_id)
        assert list(armour.keys()) == [
            "armour_id",
            "armour_type",
            "ac",
            "dr",
            "weight_class",
            "mv",
            "cost",
            "weight",
            "description",
        ]


def test_starting_shield():
    for class_id in VALID_CLASS_IDS:
        shield = get_starting_shield(class_id)
        if class_id in [1, 9, 27]:
            assert shield == {
                "shield_id": 2,
                "shield_type": "Large Shield",
                "def_mod": 2,
                "cost": 10,
                "weight": 10,
            }
        elif class_id in [5, 7, 24, 26, 31, 32, 33]:
            assert shield == {
                "shield_id": 1,
                "shield_type": "Small Shield",
                "def_mod": 1,
                "cost": 5,
                "weight": 5,
            }
        else:
            assert shield is None


def test_starting_weapons_melee():
    for class_id in VALID_CLASS_IDS:
        melee_weapons = get_starting_weapons_melee(class_id)
        assert 1 <= len(melee_weapons) <= 3


def test_starting_weapons_missile():
    for class_id in VALID_CLASS_IDS:
        missile_weapons = get_starting_weapons_missile(class_id)
        if class_id == 8:
            assert len(missile_weapons) == 2
        else:
            assert len(missile_weapons) in [0, 1]


def test_unskilled_penalty():
    for class_id in VALID_CLASS_IDS:
        assert (
            get_unskilled_weapon_penalty(class_id)
            == VALID_UNSKILLED_PENALTIES[class_id]
        )


def test_get_favoured_weapons():
    for class_id in VALID_CLASS_IDS:
        print(f"{class_id=}")
        favoured_weapons = get_favoured_weapons(class_id)
        actual_melee_wpn_ids = [
            x["weapon_id"] for x in favoured_weapons["weapons_melee"]
        ]
        actual_missile_wpn_ids = [
            x["weapon_id"] for x in favoured_weapons["weapons_missile"]
        ]
        expected = VALID_FAVOURED_WEAPONS[class_id]
        assert favoured_weapons["any"] == expected["any"]
        assert actual_melee_wpn_ids == expected["melee_wpns"]
        assert actual_missile_wpn_ids == expected["missile_wpns"]
        assert favoured_weapons["unskilled_penalty"] == expected["unskilled_penalty"]


def test_get_starting_gear():
    for class_id in VALID_CLASS_IDS:
        equip = get_starting_gear(class_id)
        assert len(equip) > 0
        for item in equip:
            assert isinstance(item, str)


def test_get_starting_money():
    for i in range(100):
        money = get_starting_money()
        assert list(money.keys()) == VALID_DENOMINATIONS
        for k in VALID_DENOMINATIONS:
            if k == "gp":
                assert money[k] in VALID_GP
            else:
                assert money[k] == 0


def test_calculate_ac():
    for class_id in VALID_CLASS_IDS:
        armour = get_starting_armour(class_id)
        shield = get_starting_shield(class_id)
        shield_def_mod = shield["def_mod"] if shield is not None else 0
        for dx_score in VALID_ABILITY_SCORES:
            dx_mod = get_attr_mod("dx", dx_score)
            ac = calculate_ac(
                armour["ac"],
                shield_def_mod,
                dx_mod["def_adj"],
            )
            # all AC values for starting characters should be 1 to 11 (level 1)
            # This may need updating after we include higher-level PCs,
            #   depending on if they have any abilities that improve AC
            assert ac in range(
                1, 12
            ), f"""invalid ac:
                class_id       = {class_id}
                armour_ac      = {armour["ac"]}
                shield_def_mod = {shield_def_mod}
                dx_score       = {dx_score}
                dx_def_adj     = {dx_mod["def_adj"]}
                ac             = {ac}
            """


def test_ac_to_aac():
    for ac in range(-10, 20):
        aac = ac_to_aac(ac)
        assert ac + aac == 19


def test_get_alignment():
    for class_id in VALID_CLASS_IDS:
        alignment = get_alignment(class_id)
        if class_id in [1, 2, 3, 7, 8, 11, 13, 18, 19]:
            allowed_alignments = ["CE", "CG", "LE", "LG", "N"]
        elif class_id in [4, 24, 25, 26, 31]:
            allowed_alignments = ["CE", "CG", "LE", "N"]
        elif class_id == 10:
            allowed_alignments = ["CG", "LG", "N"]
        elif class_id in [14, 22, 30]:
            allowed_alignments = ["CE", "LE", "N"]
        elif class_id in [15, 16, 21, 23, 29, 32]:
            allowed_alignments = ["CE", "CG", "N"]
        elif class_id in [12, 28]:
            allowed_alignments = ["LE", "LG", "N"]
        elif class_id in [5, 6, 20]:
            allowed_alignments = ["CE", "CG"]
        elif class_id == 33:
            allowed_alignments = ["LE", "N"]
        elif class_id == 9:
            allowed_alignments = ["LG"]
        elif class_id == 27:
            allowed_alignments = ["LE"]
        elif class_id == 17:
            allowed_alignments = ["N"]
        else:
            raise ValueError(f"Unexpected class_id: {class_id}")

        assert (
            alignment["short_name"] in allowed_alignments
        ), f"""
            Unexpected alignment '{alignment}' not in
            allowed values {allowed_alignments}
        """


def test_get_languages():
    for race_id in VALID_RACE_IDS:
        for bonus_languages in range(-1, 4):
            languages = get_languages(race_id, bonus_languages)
            assert "Common" in languages
            assert len(languages) == len(set(languages))
            assert 1 <= len(languages) <= 5
            if bonus_languages <= 0:
                if race_id == 1:
                    assert len(languages) == 1
                else:
                    assert len(languages) == 2
            elif bonus_languages > 0:
                if race_id == 1:
                    assert len(languages) == bonus_languages + 1
                else:
                    assert len(languages) == bonus_languages + 2


@pytest.mark.repeat(20)
def test_get_deity():
    for short_align in VALID_ALIGMENTS_SHORT:
        deity = get_deity(short_align)
        assert deity["deity_name"] in VALID_DEITIES


def test_get_thief_skills():
    # classes without thief skills
    for class_id in [
        1,
        2,
        3,
        7,
        9,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        19,
        20,
        21,
        27,
        28,
        29,
        30,
    ]:
        thief_skills = get_thief_skills(class_id, 1, 10, 10, 10)
        assert (
            thief_skills is None
        ), f"class_id: {class_id} is not supposed to have thief skills"

    # level 1 thief with 10's
    expected_thief_skills = [
        {"thief_skill": "climb", "skill_name": "Climb", "skill_roll": 8, "stat": "dx"},
        {
            "thief_skill": "decipher_script",
            "skill_name": "Decipher Script",
            "skill_roll": 0,
            "stat": "in",
        },
        {
            "thief_skill": "discern_noise",
            "skill_name": "Discern Noise",
            "skill_roll": 4,
            "stat": "ws",
        },
        {"thief_skill": "hide", "skill_name": "Hide", "skill_roll": 5, "stat": "dx"},
        {
            "thief_skill": "manipulate_traps",
            "skill_name": "Manipulate Traps",
            "skill_roll": 3,
            "stat": "dx",
        },
        {
            "thief_skill": "move_silently",
            "skill_name": "Move Silently",
            "skill_roll": 5,
            "stat": "dx",
        },
        {
            "thief_skill": "open_locks",
            "skill_name": "Open Locks",
            "skill_roll": 3,
            "stat": "dx",
        },
        {
            "thief_skill": "pick_pockets",
            "skill_name": "Pick Pockets",
            "skill_roll": 4,
            "stat": "dx",
        },
        {
            "thief_skill": "read_scrolls",
            "skill_name": "Read Scrolls",
            "skill_roll": None,
            "stat": "in",
        },
    ]
    thief_skills = get_thief_skills(4, 1, 10, 10, 10)
    assert thief_skills == expected_thief_skills

    # level 1 thief with 16's
    expected_thief_skills = [
        {"thief_skill": "climb", "skill_name": "Climb", "skill_roll": 9, "stat": "dx"},
        {
            "thief_skill": "decipher_script",
            "skill_name": "Decipher Script",
            "skill_roll": 1,
            "stat": "in",
        },
        {
            "thief_skill": "discern_noise",
            "skill_name": "Discern Noise",
            "skill_roll": 5,
            "stat": "ws",
        },
        {"thief_skill": "hide", "skill_name": "Hide", "skill_roll": 6, "stat": "dx"},
        {
            "thief_skill": "manipulate_traps",
            "skill_name": "Manipulate Traps",
            "skill_roll": 4,
            "stat": "dx",
        },
        {
            "thief_skill": "move_silently",
            "skill_name": "Move Silently",
            "skill_roll": 6,
            "stat": "dx",
        },
        {
            "thief_skill": "open_locks",
            "skill_name": "Open Locks",
            "skill_roll": 4,
            "stat": "dx",
        },
        {
            "thief_skill": "pick_pockets",
            "skill_name": "Pick Pockets",
            "skill_roll": 5,
            "stat": "dx",
        },
        {
            "thief_skill": "read_scrolls",
            "skill_name": "Read Scrolls",
            "skill_roll": None,
            "stat": "in",
        },
    ]
    thief_skills = get_thief_skills(4, 1, 16, 16, 16)
    assert thief_skills == expected_thief_skills

    # level 12 thief with 10's
    expected_thief_skills = [
        {"thief_skill": "climb", "skill_name": "Climb", "skill_roll": 10, "stat": "dx"},
        {
            "thief_skill": "decipher_script",
            "skill_name": "Decipher Script",
            "skill_roll": 5,
            "stat": "in",
        },
        {
            "thief_skill": "discern_noise",
            "skill_name": "Discern Noise",
            "skill_roll": 9,
            "stat": "ws",
        },
        {"thief_skill": "hide", "skill_name": "Hide", "skill_roll": 10, "stat": "dx"},
        {
            "thief_skill": "manipulate_traps",
            "skill_name": "Manipulate Traps",
            "skill_roll": 8,
            "stat": "dx",
        },
        {
            "thief_skill": "move_silently",
            "skill_name": "Move Silently",
            "skill_roll": 10,
            "stat": "dx",
        },
        {
            "thief_skill": "open_locks",
            "skill_name": "Open Locks",
            "skill_roll": 8,
            "stat": "dx",
        },
        {
            "thief_skill": "pick_pockets",
            "skill_name": "Pick Pockets",
            "skill_roll": 9,
            "stat": "dx",
        },
        {
            "thief_skill": "read_scrolls",
            "skill_name": "Read Scrolls",
            "skill_roll": 5,
            "stat": "in",
        },
    ]
    thief_skills = get_thief_skills(4, 12, 10, 10, 10)
    assert thief_skills == expected_thief_skills

    # level 12 thief with 16's
    expected_thief_skills = [
        {"thief_skill": "climb", "skill_name": "Climb", "skill_roll": 11, "stat": "dx"},
        {
            "thief_skill": "decipher_script",
            "skill_name": "Decipher Script",
            "skill_roll": 6,
            "stat": "in",
        },
        {
            "thief_skill": "discern_noise",
            "skill_name": "Discern Noise",
            "skill_roll": 10,
            "stat": "ws",
        },
        {"thief_skill": "hide", "skill_name": "Hide", "skill_roll": 11, "stat": "dx"},
        {
            "thief_skill": "manipulate_traps",
            "skill_name": "Manipulate Traps",
            "skill_roll": 9,
            "stat": "dx",
        },
        {
            "thief_skill": "move_silently",
            "skill_name": "Move Silently",
            "skill_roll": 11,
            "stat": "dx",
        },
        {
            "thief_skill": "open_locks",
            "skill_name": "Open Locks",
            "skill_roll": 9,
            "stat": "dx",
        },
        {
            "thief_skill": "pick_pockets",
            "skill_name": "Pick Pockets",
            "skill_roll": 10,
            "stat": "dx",
        },
        {
            "thief_skill": "read_scrolls",
            "skill_name": "Read Scrolls",
            "skill_roll": 6,
            "stat": "in",
        },
    ]
    thief_skills = get_thief_skills(4, 12, 16, 16, 16)
    assert thief_skills == expected_thief_skills

    # validate all classes with thief skills
    for class_id in [4, 5, 6, 8, 10, 18, 22, 23, 24, 25, 26, 31, 32, 33]:
        thief_skills = get_thief_skills(class_id, 1, 10, 10, 10)
        if thief_skills:
            assert [
                x["thief_skill"] for x in thief_skills
            ] == VALID_CLASS_THIEF_ABILITIES[class_id]
        else:
            raise ValueError(
                "thief_skills empty for class that is supposed to have them"
            )

    # invalid class_id should raise exception
    with pytest.raises(ValueError):
        get_thief_skills(class_id=34, level=1, dx_score=10, in_score=10, ws_score=10)
    # invalid level should raise exception
    with pytest.raises(ValueError):
        get_thief_skills(class_id=1, level=13, dx_score=10, in_score=10, ws_score=10)
    # invalid_ability scores should raise exception
    with pytest.raises(ValueError):
        get_thief_skills(class_id=1, level=1, dx_score=19, in_score=10, ws_score=10)
    with pytest.raises(ValueError):
        get_thief_skills(class_id=1, level=1, dx_score=10, in_score=19, ws_score=10)
    with pytest.raises(ValueError):
        get_thief_skills(class_id=1, level=1, dx_score=10, in_score=10, ws_score=19)


def test_get_caster_schools():
    for class_id in VALID_CLASS_IDS:
        schools = get_caster_schools(class_id)
        if class_id == 21:
            assert schools in [
                ["clr", "mag"],
                ["clr", "nec"],
                ["drd", "mag"],
                ["drd", "nec"],
            ]
        else:
            assert schools == VALID_SCHOOLS_BY_CLASS_ID[class_id]


def test_get_turn_undead_matrix():
    for ta in VALID_TA:
        for turn_adj in [-1, 0, 1]:
            turn_undead_matrix = get_turn_undead_matrix(ta, turn_adj)
            if ta == 0:
                assert turn_undead_matrix is None
            if ta == 1 and turn_adj == -1:
                assert turn_undead_matrix == {
                    "undead_type_00": "9:12",
                    "undead_type_01": "6:12",
                    "undead_type_02": "3:12",
                    "undead_type_03": "NT",
                    "undead_type_04": "NT",
                    "undead_type_05": "NT",
                    "undead_type_06": "NT",
                    "undead_type_07": "NT",
                    "undead_type_08": "NT",
                    "undead_type_09": "NT",
                    "undead_type_10": "NT",
                    "undead_type_11": "NT",
                    "undead_type_12": "NT",
                    "undead_type_13": "NT",
                }
            if ta == 1 and turn_adj == 0:
                assert turn_undead_matrix == {
                    "undead_type_00": "10:12",
                    "undead_type_01": "7:12",
                    "undead_type_02": "4:12",
                    "undead_type_03": "1:12",
                    "undead_type_04": "NT",
                    "undead_type_05": "NT",
                    "undead_type_06": "NT",
                    "undead_type_07": "NT",
                    "undead_type_08": "NT",
                    "undead_type_09": "NT",
                    "undead_type_10": "NT",
                    "undead_type_11": "NT",
                    "undead_type_12": "NT",
                    "undead_type_13": "NT",
                }
            if ta == 12 and turn_adj == 0:
                assert turn_undead_matrix == {
                    "undead_type_00": "UD",
                    "undead_type_01": "UD",
                    "undead_type_02": "UD",
                    "undead_type_03": "UD",
                    "undead_type_04": "UD",
                    "undead_type_05": "UD",
                    "undead_type_06": "D",
                    "undead_type_07": "D",
                    "undead_type_08": "D",
                    "undead_type_09": "T",
                    "undead_type_10": "T",
                    "undead_type_11": "10:12",
                    "undead_type_12": "7:12",
                    "undead_type_13": "4:12",
                }
            if ta == 12 and turn_adj == 1:
                assert turn_undead_matrix == {
                    "undead_type_00": "UD",
                    "undead_type_01": "UD",
                    "undead_type_02": "UD",
                    "undead_type_03": "UD",
                    "undead_type_04": "UD",
                    "undead_type_05": "UD",
                    "undead_type_06": "D",
                    "undead_type_07": "D",
                    "undead_type_08": "D",
                    "undead_type_09": "T",
                    "undead_type_10": "T",
                    "undead_type_11": "11:12",
                    "undead_type_12": "8:12",
                    "undead_type_13": "5:12",
                }


def test_spell_data():
    for school in VALID_SCHOOLS:
        for spell_level in VALID_SPELL_LEVELS:
            for d100_roll in range(1, 101):
                spell = get_random_spell(school, spell_level, d100_roll)
                assert spell is not None


def test_get_random_spell():
    for school in VALID_SCHOOLS:
        for spell_level in VALID_SPELL_LEVELS:
            for i in range(1000):
                spell = get_random_spell(school, spell_level)
                assert spell["school"] == school
                assert spell["spell_level"] == spell_level
                assert spell["reversible"] in [None, True, False]
    # invalid input should raise an exception
    with pytest.raises(AssertionError):
        get_random_spell(school="FakeSchool", spell_level=1)
    with pytest.raises(AssertionError):
        get_random_spell(school="mag", spell_level=7)
    with pytest.raises(AssertionError):
        get_random_spell(school="mag", spell_level=1, d100_roll=101)


def test_get_spells():
    for class_id in VALID_CLASS_IDS:
        for level in VALID_LEVELS:
            cl_data = get_class_level_data(class_id, level)
            ca = cl_data["ca"]
            spells = get_spells(class_id, level, ca)
            if ca > 0:
                assert spells, f"{class_id=} {level=} {spells=}"
                schools = list(spells.keys())
            else:
                assert spells is None
                schools = []

            if ca > 1 and class_id != 21:
                assert schools == VALID_SCHOOLS_BY_CLASS_ID[class_id]
            elif class_id == 21:
                assert schools in [
                    ["clr", "mag"],
                    ["clr", "nec"],
                    ["drd", "mag"],
                    ["drd", "nec"],
                ]

            # classes without spells
            if ca == 0:
                assert spells is None, f"{class_id=} {level=}"
            # classes with no spells at early levels


def test_get_random_familiar():
    for i in range(1000):
        animal = get_random_familiar()
        assert animal in VALID_FAMILIARS, f"{animal=} not in {VALID_FAMILIARS}"


def test_get_secondary_skill():
    secondary_skill = get_secondary_skill()
    assert secondary_skill in VALID_SECONDARY_SKILLS


def test_inches_to_feet():
    assert inches_to_feet(60) == "5'0\""
    assert inches_to_feet(65) == "5'5\""
    assert inches_to_feet(70) == '''5'10"'''
    assert inches_to_feet(75) == '''6'3"'''


@pytest.mark.repeat(1000)
def test_get_height_weight_lookup_vals():
    for race_id in VALID_RACE_IDS:
        for gender in VALID_GENDERS:
            lookup_roll, lookup_gender = get_height_weight_lookup_vals(race_id, gender)
            assert 3 <= lookup_roll <= 18
            assert lookup_gender in ["Female", "Male"]
            if race_id == 2 and lookup_gender == "Female":
                assert lookup_roll >= 6
            if race_id in [10, 11, 17, 20]:
                assert lookup_roll <= 15
            if race_id == 5:
                assert lookup_roll in [17, 18]
            if race_id == 21:
                assert 9 <= lookup_roll <= 12


def test_get_height_and_weight():
    for race_id in VALID_RACE_IDS:
        for gender in VALID_GENDERS:
            height, weight = get_height_and_weight(race_id, gender)
            height_ft = int(height.split("'")[0])
            height_in = int(height.split("'")[1].replace('"', ""))
            weight_num = int(weight.split()[0])
            weight_units = weight.split()[-1]
            assert 0 <= height_in <= 11
            assert weight_units == "lbs."
            if gender == "Male":
                assert 5 <= height_ft <= 7
                assert 96 <= weight_num <= 350
            elif gender == "Female":
                assert 4 <= height_ft <= 6
                assert 68 <= weight_num <= 273
            else:
                assert 4 <= height_ft <= 7
                assert 68 <= weight_num <= 350


def test_get_eye_colour():
    for race_id in VALID_RACE_IDS:
        for gender in VALID_GENDERS:
            eye_colour = get_eye_colour(race_id, gender)
            assert eye_colour in VALID_EYE_COLOURS


def test_get_hair_colour():
    for race_id in VALID_RACE_IDS:
        for gender in VALID_GENDERS:
            hair_colour = get_hair_colour(race_id, gender)
            assert hair_colour in VALID_HAIR_COLOURS


def test_get_complexion():
    for race_id in VALID_RACE_IDS:
        for gender in VALID_GENDERS:
            complexion = get_complexion(race_id, gender)
            assert complexion in VALID_COMPLEXIONS


def test_select_random_class():
    attr = get_attr()
    class_id = select_random_class(attr=attr, subclasses=2)
    assert class_id in VALID_CLASS_IDS
