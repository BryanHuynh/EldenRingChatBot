
from elden_ring_wiki.tools.splitters.md_splitter import WikiChildSplitter



def load_test_data():
    data = """
## Bell Bearing Hunter  
  
---  
Locations & Drops  
Warmaster's Shack:  
2,700 Runes (NG)  
675 Runes (NG, Co-op)  
Bone Peddler's Bell Bearing Church of Vows:  
6,000 Runes  
(NG)  
4,500 Runes (NG, Co-op Host)  
1,500 Runes (NG, Co-op Phantom)  
Meat Peddler's Bell Bearing Hermit Merchant's Shack:  
20,000 Runes (NG)  
15,000 Runes (NG, Co-op Host)  
5,000 Runes (NG, Co-op Phantom)  
Medicine Peddler's Bell Bearing Isolated Merchant's Shack (Dragonbarrow):  
50,000  
Gravity Stone Peddler's Bell Bearing  
Stronger VS  Hemorrhage   
Frostbite | Weaker to  
Pierce   
Lightning  
  
Bell Bearing Hunter is a recurring Field Boss in Elden Ring. He is a hunter of shopkeepers who only appears at night and features long-distance melee attacks. This is an optional boss as players don't need to defeat it to advance in Elden Ring.

He will appear only at night, so if you don't see him, make sure to rest again at the nearby Site of Grace after passing time to nightfall.

See Elemer of the Briar for the Great Enemy version of this boss. Defeating the real Elemer will not prevent the Bell Bearing Hunters from appearing, however. Despite his fearsome reputation, the Bell Bearing Hunter cannot permanently kill merchants.

See Bell Bearing Hunter Lore

> Elemer murdered numerous instructors and merchants, and was known as the Bell Bearing Hunter.

### Elden Ring Bell Bearing Hunter Locations

  * Warmaster's Shack [More Info] [Map Link]
  * Church of Vows [More Info] [Map Link] 
  * Hermit Merchant's Shack [More Info] [Map Link]
  * Isolated Merchant's Shack (Dragonbarrow) [More Info] [Map Link]
  * Bell Bearing Hunter only spawns provided 3 requirements (in this order it will be faster): 1. The player needs to rest at the near site of grace; 2. It must be night; 3. The player needs to trigger the title of the specific location (like "Warmaster's Shack").  

    * Players can simply rest at the locations Site of Grace, skip time until night, then exit and re-enter the game to get the boss to spawn. 



### Bell Bearing Hunter Combat information

  * Stance: 80
  * Parryable: Yes, but 2 parries are required per stance break
  * Is vulnerable to a  critical hit  after being stance broken or parried
  * Damage: Standard, Strike, Pierce, Magic
  * See Elemer of the Briar for a full boss guide
  * If you can climb on nearby scenery and get above the Bell Bearing Hunter's head, none of his attacks can hit you. Use spells like Night Maiden's Mist that can hit through structures to damage him. Even if it seems like he's going out of range, you can simply wait and he will be back in a moment.
  * If you have sufficient health, you can use Lion's Claw to tank his hits as the startup animation has superarmor which means you can't be staggered out of it by most attacks. Hit him enough times to stance break him, perform a critical and then heal while he is getting up. You will still need enough health to tank his hits and enough damage to kill him before you run out of flasks.
"""
    return data


def test_split():
    splitter = WikiChildSplitter()
    data = load_test_data()
    chunks = splitter.split_text(data)
    assert len(chunks) > 0
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i + 1} ---")
        print(chunk)
        print()