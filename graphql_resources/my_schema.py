import sgqlc.types


my_schema = sgqlc.types.Schema()


__docformat__ = "markdown"


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################


########################################################################
# Output Objects and Interfaces
########################################################################
class Ammo(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "type",
        "attack_power",
        "passive",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(String, graphql_name="type")

    attack_power = sgqlc.types.Field(
        sgqlc.types.list_of("AttributeEntry"), graphql_name="attackPower"
    )

    passive = sgqlc.types.Field(String, graphql_name="passive")


class Armor(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "category",
        "dmg_negation",
        "resistance",
        "weight",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    category = sgqlc.types.Field(String, graphql_name="category")

    dmg_negation = sgqlc.types.Field(
        sgqlc.types.list_of("AttributeEntry"), graphql_name="dmgNegation"
    )

    resistance = sgqlc.types.Field(
        sgqlc.types.list_of("AttributeEntry"), graphql_name="resistance"
    )

    weight = sgqlc.types.Field(Float, graphql_name="weight")


class AshOfWar(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "image", "description", "affinity", "skill")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    affinity = sgqlc.types.Field(String, graphql_name="affinity")

    skill = sgqlc.types.Field(String, graphql_name="skill")


class AttributeEntryNames(sgqlc.types.Enum):
    __schema__ = my_schema
    __choices__ = (
        "Phy",
        "Mag",
        "Fire",
        "Ligt",
        "Holy",
        "Crit",
    )


class AttributeEntry(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("amount", "name")
    amount = sgqlc.types.Field(Int, graphql_name="amount")

    name = sgqlc.types.Field(AttributeEntryNames, graphql_name="name")


class Boss(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "location",
        "drops",
        "health_points",
        "region",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    location = sgqlc.types.Field(String, graphql_name="location")

    drops = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="drops")

    health_points = sgqlc.types.Field(String, graphql_name="healthPoints")

    region = sgqlc.types.Field(String, graphql_name="region")


class Class(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "image", "description", "stats")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    stats = sgqlc.types.Field("ClassStats", graphql_name="stats")


class ClassStats(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "level",
        "vigor",
        "mind",
        "endurance",
        "strenght",
        "dexterity",
        "inteligence",
        "faith",
        "arcane",
    )
    level = sgqlc.types.Field(String, graphql_name="level")

    vigor = sgqlc.types.Field(String, graphql_name="vigor")

    mind = sgqlc.types.Field(String, graphql_name="mind")

    endurance = sgqlc.types.Field(String, graphql_name="endurance")

    strenght = sgqlc.types.Field(String, graphql_name="strenght")

    dexterity = sgqlc.types.Field(String, graphql_name="dexterity")

    inteligence = sgqlc.types.Field(String, graphql_name="inteligence")

    faith = sgqlc.types.Field(String, graphql_name="faith")

    arcane = sgqlc.types.Field(String, graphql_name="arcane")


class Creature(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "image", "description", "location", "drops")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    location = sgqlc.types.Field(String, graphql_name="location")

    drops = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="drops")


class Incantation(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "type",
        "cost",
        "slots",
        "effects",
        "requires",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(String, graphql_name="type")

    cost = sgqlc.types.Field(Int, graphql_name="cost")

    slots = sgqlc.types.Field(Int, graphql_name="slots")

    effects = sgqlc.types.Field(String, graphql_name="effects")

    requires = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="requires"
    )


class Item(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "image", "description", "effect", "type")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    effect = sgqlc.types.Field(String, graphql_name="effect")

    type = sgqlc.types.Field(String, graphql_name="type")


class Location(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "image", "description", "region")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    region = sgqlc.types.Field(String, graphql_name="region")


class Npc(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "quote",
        "location",
        "role",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    quote = sgqlc.types.Field(String, graphql_name="quote")

    location = sgqlc.types.Field(String, graphql_name="location")

    role = sgqlc.types.Field(String, graphql_name="role")


class Query(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "ammo",
        "get_ammo",
        "armor",
        "get_armor",
        "ash_of_war",
        "get_ash_of_war",
        "boss",
        "get_boss",
        "class_",
        "get_class",
        "creature",
        "get_creature",
        "incantation",
        "get_incantation",
        "item",
        "get_item",
        "location",
        "get_location",
        "npc",
        "get_npc",
        "shield",
        "get_shield",
        "sorcery",
        "get_sorcery",
        "spirit",
        "get_spirit",
        "talisman",
        "get_talisman",
        "weapon",
        "get_weapon",
    )
    ammo = sgqlc.types.Field(
        sgqlc.types.list_of(Ammo),
        graphql_name="ammo",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                ("type", sgqlc.types.Arg(String, graphql_name="type", default=None)),
                (
                    "passive",
                    sgqlc.types.Arg(String, graphql_name="passive", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `type` (`String`)
    * `passive` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_ammo = sgqlc.types.Field(
        sgqlc.types.non_null(Ammo),
        graphql_name="getAmmo",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    armor = sgqlc.types.Field(
        sgqlc.types.list_of(Armor),
        graphql_name="armor",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "category",
                    sgqlc.types.Arg(String, graphql_name="category", default=None),
                ),
                ("weight", sgqlc.types.Arg(Float, graphql_name="weight", default=None)),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `category` (`String`)
    * `weight` (`Float`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_armor = sgqlc.types.Field(
        sgqlc.types.non_null(Armor),
        graphql_name="getArmor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    ash_of_war = sgqlc.types.Field(
        sgqlc.types.list_of(AshOfWar),
        graphql_name="ashOfWar",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "affinity",
                    sgqlc.types.Arg(String, graphql_name="affinity", default=None),
                ),
                ("skill", sgqlc.types.Arg(String, graphql_name="skill", default=None)),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `affinity` (`String`)
    * `skill` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_ash_of_war = sgqlc.types.Field(
        sgqlc.types.non_null(AshOfWar),
        graphql_name="getAshOfWar",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    boss = sgqlc.types.Field(
        sgqlc.types.list_of(Boss),
        graphql_name="boss",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "location",
                    sgqlc.types.Arg(String, graphql_name="location", default=None),
                ),
                (
                    "health_points",
                    sgqlc.types.Arg(String, graphql_name="healthPoints", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "region",
                    sgqlc.types.Arg(String, graphql_name="region", default=None),
                ),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `location` (`String`)
    * `health_points` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `region` (`String`)
    * `search` (`String`)
    """

    get_boss = sgqlc.types.Field(
        sgqlc.types.non_null(Boss),
        graphql_name="getBoss",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    class_ = sgqlc.types.Field(
        sgqlc.types.list_of(Class),
        graphql_name="class",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_class = sgqlc.types.Field(
        sgqlc.types.non_null(Class),
        graphql_name="getClass",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    creature = sgqlc.types.Field(
        sgqlc.types.list_of(Creature),
        graphql_name="creature",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "location",
                    sgqlc.types.Arg(String, graphql_name="location", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `location` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_creature = sgqlc.types.Field(
        sgqlc.types.non_null(Creature),
        graphql_name="getCreature",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    incantation = sgqlc.types.Field(
        sgqlc.types.list_of(Incantation),
        graphql_name="incantation",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                ("type", sgqlc.types.Arg(String, graphql_name="type", default=None)),
                ("cost", sgqlc.types.Arg(Int, graphql_name="cost", default=None)),
                ("slots", sgqlc.types.Arg(Int, graphql_name="slots", default=None)),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `type` (`String`)
    * `cost` (`Int`)
    * `slots` (`Int`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_incantation = sgqlc.types.Field(
        sgqlc.types.non_null(Incantation),
        graphql_name="getIncantation",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    item = sgqlc.types.Field(
        sgqlc.types.list_of(Item),
        graphql_name="item",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "effect",
                    sgqlc.types.Arg(String, graphql_name="effect", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `effect` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_item = sgqlc.types.Field(
        sgqlc.types.non_null(Item),
        graphql_name="getItem",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    location = sgqlc.types.Field(
        sgqlc.types.list_of(Location),
        graphql_name="location",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "region",
                    sgqlc.types.Arg(String, graphql_name="region", default=None),
                ),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `region` (`String`)
    * `search` (`String`)
    """

    get_location = sgqlc.types.Field(
        sgqlc.types.non_null(Location),
        graphql_name="getLocation",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    npc = sgqlc.types.Field(
        sgqlc.types.list_of(Npc),
        graphql_name="npc",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                ("quote", sgqlc.types.Arg(String, graphql_name="quote", default=None)),
                (
                    "location",
                    sgqlc.types.Arg(String, graphql_name="location", default=None),
                ),
                ("role", sgqlc.types.Arg(String, graphql_name="role", default=None)),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `quote` (`String`)
    * `location` (`String`)
    * `role` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_npc = sgqlc.types.Field(
        sgqlc.types.non_null(Npc),
        graphql_name="getNpc",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    shield = sgqlc.types.Field(
        sgqlc.types.list_of("Shield"),
        graphql_name="shield",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "category",
                    sgqlc.types.Arg(String, graphql_name="category", default=None),
                ),
                ("weight", sgqlc.types.Arg(Float, graphql_name="weight", default=None)),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `category` (`String`)
    * `weight` (`Float`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_shield = sgqlc.types.Field(
        sgqlc.types.non_null("Shield"),
        graphql_name="getShield",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    sorcery = sgqlc.types.Field(
        sgqlc.types.list_of("Sorcery"),
        graphql_name="sorcery",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                ("type", sgqlc.types.Arg(String, graphql_name="type", default=None)),
                ("cost", sgqlc.types.Arg(Int, graphql_name="cost", default=None)),
                ("slots", sgqlc.types.Arg(Int, graphql_name="slots", default=None)),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `type` (`String`)
    * `cost` (`Int`)
    * `slots` (`Int`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_sorcery = sgqlc.types.Field(
        sgqlc.types.non_null("Sorcery"),
        graphql_name="getSorcery",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    spirit = sgqlc.types.Field(
        sgqlc.types.list_of("Spirit"),
        graphql_name="spirit",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "fp_cost",
                    sgqlc.types.Arg(String, graphql_name="fpCost", default=None),
                ),
                (
                    "hp_cost",
                    sgqlc.types.Arg(String, graphql_name="hpCost", default=None),
                ),
                (
                    "effect",
                    sgqlc.types.Arg(String, graphql_name="effect", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `fp_cost` (`String`)
    * `hp_cost` (`String`)
    * `effect` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_spirit = sgqlc.types.Field(
        sgqlc.types.non_null("Spirit"),
        graphql_name="getSpirit",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    talisman = sgqlc.types.Field(
        sgqlc.types.list_of("Talisman"),
        graphql_name="talisman",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "effect",
                    sgqlc.types.Arg(String, graphql_name="effect", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `effect` (`String`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_talisman = sgqlc.types.Field(
        sgqlc.types.non_null("Talisman"),
        graphql_name="getTalisman",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """

    weapon = sgqlc.types.Field(
        sgqlc.types.list_of("Weapon"),
        graphql_name="weapon",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "category",
                    sgqlc.types.Arg(String, graphql_name="category", default=None),
                ),
                ("weight", sgqlc.types.Arg(Float, graphql_name="weight", default=None)),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `name` (`String`)
    * `description` (`String`)
    * `category` (`String`)
    * `weight` (`Float`)
    * `page` (`Int`) (default: `0`)
    * `limit` (`Int`)
    * `search` (`String`)
    """

    get_weapon = sgqlc.types.Field(
        sgqlc.types.non_null("Weapon"),
        graphql_name="getWeapon",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`String!`)
    """


class ScalingEntryNames(sgqlc.types.Enum):
    __schema__ = my_schema
    __choices__ = ("STR", "DEX", "INT", "FTH", "ARC")


class ScalingEntryScaling(sgqlc.types.Enum):
    __schema__ = my_schema
    __choices__ = ("S", "A", "B", "C", "D", "E", "None")


class ScalingEntry(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("scaling", "name")
    scaling = sgqlc.types.Field(ScalingEntryScaling, graphql_name="scaling")
    name = sgqlc.types.Field(ScalingEntryNames, graphql_name="name")


class Shield(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "attack",
        "defence",
        "scalesWith",
        "requiredAttributes",
        "category",
        "weight",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    attack = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="attack"
    )

    defence = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="defence"
    )

    scalesWith = sgqlc.types.Field(
        sgqlc.types.list_of(ScalingEntry), graphql_name="scalesWith"
    )

    requiredAttributes = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="requiredAttributes"
    )

    category = sgqlc.types.Field(String, graphql_name="category")

    weight = sgqlc.types.Field(Float, graphql_name="weight")


class Sorcery(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "type",
        "cost",
        "slots",
        "effects",
        "requires",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(String, graphql_name="type")

    cost = sgqlc.types.Field(Int, graphql_name="cost")

    slots = sgqlc.types.Field(Int, graphql_name="slots")

    effects = sgqlc.types.Field(String, graphql_name="effects")

    requires = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="requires"
    )


class Spirit(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "fp_cost",
        "hp_cost",
        "effect",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    fp_cost = sgqlc.types.Field(String, graphql_name="fpCost")

    hp_cost = sgqlc.types.Field(String, graphql_name="hpCost")

    effect = sgqlc.types.Field(String, graphql_name="effect")


class Talisman(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "image", "description", "effect")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    effect = sgqlc.types.Field(String, graphql_name="effect")


class Weapon(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "name",
        "image",
        "description",
        "attack",
        "defence",
        "scalesWith",
        "requiredAttributes",
        "category",
        "weight",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    image = sgqlc.types.Field(String, graphql_name="image")

    description = sgqlc.types.Field(String, graphql_name="description")

    attack = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="attack"
    )

    defence = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="defence"
    )

    scalesWith = sgqlc.types.Field(
        sgqlc.types.list_of(ScalingEntry), graphql_name="scalesWith"
    )

    requiredAttributes = sgqlc.types.Field(
        sgqlc.types.list_of(AttributeEntry), graphql_name="requiredAttributes"
    )

    category = sgqlc.types.Field(String, graphql_name="category")

    weight = sgqlc.types.Field(Float, graphql_name="weight")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
my_schema.query_type = Query
my_schema.mutation_type = None
my_schema.subscription_type = None
