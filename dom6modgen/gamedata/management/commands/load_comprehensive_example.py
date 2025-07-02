# dom6modgen/gamedata/management/commands/load_comprehensive_example.py

from django.core.management.base import BaseCommand
from gamedata.models import ModExample

class Command(BaseCommand):
    help = 'Loads the comprehensive mod example into the ModExample database table.'

    def handle(self, *args, **options):
        # The content of your comprehensive_mod_example immersive
        # Ensure the triple quotes are correct for a multi-line string
        mod_text_content = """#modname "Comprehensive Mod Examples"
#description "This mod provides examples for various Dominions 6 modding categories, extracted from existing mod files."
#version 1.0
#domversion 6.00

-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////
--                         NATION DETAILS EXAMPLES
-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////

-- Example 1: From Forgotten Realms (Nation 203 - Calimshan)
#selectnation 203
#name "Example Nation: Calimshan"
#epithet "Lands of Intrigue"
#era 2
#brief "The history of the Calishites led them to have deeply rooted ties to the genies that had long since left the lands."
#summary "All the paths of magic are openly practiced in Calimshan, and you have supreme access to the many faiths of Faerun. Don't get overwhelmed. Coastal provinces bring extra income. Mechants as well. Protect your capital and expand your overseas empire with lots of sailing commanders."
#color 0.9 0.8 0.2
#flag "ForgottenRealms/flag203.tga"
#templepic 5
#idealcold -1
#coastnation
#labcost 400
#templecost 400
#end

-- Example 2: From Confluence (Nation 317 - Abysia Reborn)
#selectnation 317
#name "Example Nation: Abysia Reborn"
#epithet "Children of Flame"
#era 1
#brief "Abysians are lava-born humanoids that radiate heat. Abysians mainly use heavy infantry. They have skilled Fire and Blood mages and their priests can perform blood sacrifices. Abysians dislike cold provinces."
#summary "Race: Humanoids. Radiate heat and prefers Heat scales. Wasteland survival. Death/Growth scales have halved effect on income and population growth, and no effect on supplies."
#color 1 0 0
#flag "./Confluence/EA_Abysia Reborn/Abysia_Reborn_flag.tga"
#templepic 0
#idealcold -3
#spreadheat 3
#nodeathsupply
#halfdeathinc
#halfdeathpop
#end

-- Example 3: From Sombre Warhammer (Nation 151 - Athel Loren)
#selectnation 151
#name "Example Nation: Athel Loren"
#epithet "Forest of the Asrai"
#era 2
#brief "The Asrai, or Wood Elves as some call them, are an offshoot of the Elven people of Ulthuan who long ago split from the Elven empire which once spanned the world to shelter in the ancient forest of Athel Loren."
#summary "Race: Graceful elves and forest spirits. Military: Superb archers, skilled infantry, sacred cavalary, and spiteful forest spirits. All troops gain bonuses in forest provinces."
#color .0 .6 .0
#flag "Sombre_Warhammer/Warhammer_Wood_Elves/Wood_Elf_Flag.tga"
#templepic 10
#moremagic 1
#moregrowth 2
#idealcold 0
#likesterr 128
#fortera 0
#homefort 3
#fortcost 20
#labcost 750
#templecost 750
#foresttemplecost 400
#forestlabcost 500
#end

-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////
--                         COMMANDER EXAMPLES
-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////

-- Example 1: Inner Sea Captain (from Forgotten Realms)
#newmonster 291
#spr1 "ForgottenRealms/innerseacaptain.tga"
#spr2 "ForgottenRealms/innerseacaptain2.tga"
#name "Inner Sea Captain"
#descr "The Sea of Fallen Stars, also known as the Inner Sea, was the largest inland body of water in Faerûn. The captains who plied these waters prayed day and night to the gods of the sea to keep them safe on their journeys."
#gcost 100
#hp 24
#prot 6
#mr 10
#mor 14
#str 10
#att 12
#def 12
#prec 10
#ap 12
#mapmove 14
#enc 3
#weapon 10 -- falchion
#armor 6 -- ring mail cuirass
#stealthy 15
#goodleader
#sailing 999 6
#patrolbonus 2
#end

-- Example 2: Pyremaster (from Confluence/Abysia Reborn)
#newmonster 16946
#spr1 "./Confluence/EA_Abysia Reborn/Commander1.tga"
#spr2 "./Confluence/EA_Abysia Reborn/Commander2.tga"
#name "Pyremaster"
#descr "Pyremasters are the generals of Abysian armies, chosen from among their most experienced and capable warriors who have proved their mettle in grueling campaigns, and earned the respect of their peers."
#gcost 110
#hp 19
#prot 0
#mr 13
#mor 13
#str 13
#att 11
#def 9
#prec 10
#ap 11
#mapmove 12
#enc 2
#weapon 1067 -- Burning Axe
#firepower 1
#coldres -5
#deathfire 1
#magicbeing
#goodmagicleader
#fearofflood 3
#end

-- Example 3: Glade Captain (from Sombre Warhammer/Wood Elves)
#newmonster 14137
#spr1 "Sombre_Warhammer/Warhammer_Wood_Elves/Glade_Captain.tga"
#spr2 "Sombre_Warhammer/Warhammer_Wood_Elves/Glade_Captain2.tga"
#name "Glade Captain"
#descr "The Wood Elves of Athel Loren have long been ruled over by an aristocratic class known as the Highborn, whose status and power is in proportion to their responsbility to defend and maintain the lands in which their followers dwell."
#gcost 85
#hp 14
#prot 7
#mr 13
#mor 13
#str 10
#att 13
#def 13
#prec 13
#ap 14
#mapmove 14
#enc 3
#weapon 1141 -- asrai long bow
#weapon 746 -- scimitar
#armor 7 -- scale mail cuirass
#armor 119 -- reinforced leather cap
#goodleader
#command -40
#unsurr 1
#poormagicleader
#magiccommand -5
#end

-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////
--                         TROOP EXAMPLES
-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////

-- Example 1: Dwarven Shieldsman (from Forgotten Realms)
#newmonster 7186
#spr1 "ForgottenRealms/dwarvenshieldsman.tga"
#spr2 "ForgottenRealms/dwarvenshieldsman2.tga"
#name "Dwarven Shieldsman"
#descr "Armed with a dwarven tower shield and a stabbing blade, these heavy footmen are trained to stand in the front line and soak the heavy blows of their enemies, giving other elements of the dwarven army a chance to maneuver."
#gcost 18
#hp 16
#prot 26
#mr 11
#mor 16
#str 11
#att 11
#def 13
#prec 8
#ap 12
#mapmove 14
#enc 4
#weapon 6 -- Short Sword
#armor 405 -- Dwarven Full Helm
#armor 402 -- Dwarven Tower Shield
#armor 400 -- Dwarven Chainmail
#darkvision 60
#mountainsurvival
#end

-- Example 2: Abysian Infantry (from Confluence/Abysia Reborn)
#newmonster 16907
#spr1 "./Confluence/EA_Abysia Reborn/Infantry11.tga"
#spr2 "./Confluence/EA_Abysia Reborn/Infantry12.tga"
#name "Abysian Infantry"
#descr "The Abysians are a race of molten humanoids born from the cataclysmic destruction of the besieged city of Edranor. These beings radiate furnace-like heat, their veins coursing with molten rock, and their skin perpetually glowing with cracks of smoldering embers."
#gcost 8
#hp 10
#prot 18
#mr 10
#mor 9
#str 11
#att 8
#def 7
#prec 8
#ap 8
#mapmove 10
#enc 3
#weapon 1063 -- Burning Battleaxe
#firepower 1
#noriverpass
#coldres -5
#deathfire 1
#magicbeing
#fearofflood 3
#end

-- Example 3: Glade Guard (from Sombre Warhammer/Wood Elves)
#newmonster 14131
#spr1 "Sombre_Warhammer/Warhammer_Wood_Elves/Glade_Guard.tga"
#spr2 "Sombre_Warhammer/Warhammer_Wood_Elves/Glade_Guard2.tga"
#name "Glade Guard"
#descr "In time of need, every Wood Elf can answer the call to defend their realm, for all are trained in the art of the Long Bow as soon as they are old enough to hold one."
#gcost 14
#hp 8
#prot 10
#mr 10
#mor 12
#str 9
#att 12
#def 12
#prec 12
#ap 14
#mapmove 16
#enc 3
#weapon 1141 -- asrai long bow
#weapon 6 -- Short Sword
#armor 10 -- leather hauberk
#armor 120 -- leather cap
#forestsurvival
#snow
#end

-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////
--                         HERO EXAMPLES
-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////

-- Example 1: Araloth (from Sombre Warhammer/Wood Elves)
#newmonster 14188
#spr1 "Sombre_Warhammer/Warhammer_Wood_Elves/Hero_Araloth.tga"
#spr2 "Sombre_Warhammer/Warhammer_Wood_Elves/Hero_Araloth2.tga"
#name "Lord of Talsyn"
#descr "Araloth is the Champion of the Mage Queen, Consort of the Goddess Lileath, and Lord of Talsyn, known to his fellow Asrai as Araloth the Bold for his feats of implacable bravery and honour in war."
#gcost 0
#hp 24
#prot 18
#mr 18
#mor 30
#str 11
#att 17
#def 17
#prec 18
#ap 18
#mapmove 18
#enc 3
#weapon 1165 -- Skaryn the eye thief
#weapon 1166 -- Great Hunting Spear
#armor 113 -- golden helmet
#armor 196 -- golden scale mail
#expertleader
#inspirational 1
#poormagicleader
#unsurr 4
#end

-- Example 2: Skarbrand (from Sombre Warhammer/Khorne)
#newmonster 16252
#spr1 "Sombre_Warhammer/Warhammer_Khorne/Hero_Skarbrand.tga"
#spr2 "Sombre_Warhammer/Warhammer_Khorne/Hero_Skarbrand2.tga"
#name "Exiled One"
#descr "Skarbrand was once the mightiest and most favoured of Khorne's Bloodthirsters and the highest general amongst the Greater Daemons of the Blood God."
#gcost 0
#hp 82
#prot 13
#mr 21
#mor 30
#str 24
#att 18
#def 18
#prec 14
#ap 28
#mapmove 28
#enc 1
#weapon 1223 -- carnage
#weapon 1212 -- burning brass axe
#armor 311 -- chaos helm
#armor 310 -- chaos plate armour
#flying
#neednoteat
#poisonres 10
#diseaseres 100
#demon
#holy
#fear 10
#unsurr 4
#invulnerable 15
#wastesurvival
#end

-- Example 3: Goliath (from Confluence/Dur-Halam)
#newmonster 16210
#spr1 "./Confluence/EA_Dur-Halam/Goliath1.tga"
#spr2 "./Confluence/EA_Dur-Halam/Goliath2.tga"
#name "Slave King"
#descr "It is said that Goliath was born of a giant, but orphaned at birth as his mother could not bear the strain of bringing him into the world. Even as a child, he towered over the adults of his village, his size and strength considered unnatural."
#gcost 0
#hp 26
#size 4
#prot 3
#mr 14
#mor 17
#str 19
#att 14
#def 14
#prec 12
#ap 12
#mapmove 14
#enc 3
#weapon 1056 -- Star-Forged Chains
#armor "Chain Mail Hauberk"
#armor "Iron Cap"
#mountainsurvival
#forestsurvival
#noleader
#slave
#holy
#fear 5
#pillagebonus 10
#incunrest 50
#unique
#fixedname "Goliath"
#end

-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////
--                         SPELL EXAMPLES
-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////

-- Example 1: Summon Phoenix (from Confluence/Abysia Reborn)
#newspell
#name "Summon Phoenix"
#descr "A mage stands within a circle of flickering flames, and calls forth a Phoenix from the depths of the raging fire and ash. The magnificent bird erupts into existence, its fiery wings unfurling in a blaze of radiant colors."
#school 0
#researchlevel 7
#path 0 0
#pathlevel 0 5
#fatiguecost 3200
#nreff 1
#restricted 317
#effect 10021
#damage 7859
#end

-- Example 2: Worldroot Journey (from Sombre Warhammer/Wood Elves)
#newspell
#copyspell "astral travel"
#name "Worldroot Journey"
#descr "Tapping into the system of Worldroots that connects all forests across the land, the mage opens a path through which they may travel with their followers to a distant forested province."
#details "Identical to the Astral Travel spell but with different paths and a lower cost but can only be cast in a forest and target a forest."
#path 0 6 -- nature
#pathlevel 0 4 -- N4
#onlygeosrc 128 -- forest
#onlygeodst 128 -- forest
#school 4 -- enchantment
#researchlevel 6
#fatiguecost 1500
#restricted 151
#end

-- Example 3: Arcane Annulment (from Confluence/Edranor)
#newspell
#name "Arcane Annulment"
#descr "The caster channels a considerable amount of Arcana, unleashing a concentrated wave of magic that disrupts and destabilizes the flow of magic from the Astral Plane. This disruption may cause Astral Pearls to lose their innate power, leading many to disintegrate into dust."
#details "All nations loose 3d6 Astral gems from their stockpile, including Edranor. This spell will only have effect once per turn and subsequent casts will have no effect."
#restricted 315
#school 4
#researchlevel 9
#effect 10048
#provrange 0
#nolandtrace 1
#nowatertrace 1
#damage -1
#onlyfriendlydst 1
#path 0 4
#pathlevel 0 9
#nreff 1
#fatiguecost 4000
#hiddenench 1
#nextspell "Arcane Drain"
#end

-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////
--                         ITEM EXAMPLES
-- ///////////////////////////////////////////////////////////////////////////////
-- ///////////////////////////////////////////////////////////////////////////////

-- Example 1: Stormsplitter (Weapon from Forgotten Realms)
#newweapon 1800
#copyweapon 108
#name "Stormsplitter"
#len 3
#att 5
#def 5
#dmg 18
#secondaryeffect 232 -- shock
#end

-- Example 2: Dwarven Platemail (Armor from Forgotten Realms)
#newarmor 401
#copyarmor 215 -- full plate of ulm
#name "Dwarven Platemail"
#end

-- Example 3: Ring of Power (Misc Item from Confluence/Abysia Reborn)
#selectitem 1077
#spr "./Confluence/EA_Abysia Reborn/OneRing.tga"
#name "Ring of Power"
#descr "Forged in the molten depths of Mount Ignarius, the Ring of Power is infused with the power of the volcano itself. Crafted from cooled lava and imbued with the essence of fire, the ring radiates the searing heat of Mount Ignarius and grants its bearer dominion over fire."
#type 8
#constlevel 9
#mainpath 0
#mainlevel 7
#restricted 317
#autospell "Ignarius Storm"
#autospellrepeat 1
#unique
#end
"""
        self.stdout.write(self.style.SUCCESS('Deleting existing ModExample entries...'))
        ModExample.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing ModExample entries deleted.'))

        self.stdout.write(self.style.SUCCESS('Creating new ModExample entry for Comprehensive Mod Example...'))
        ModExample.objects.create(
            name="Comprehensive Mod Example",
            mod_text=mod_text_content
        )
        self.stdout.write(self.style.SUCCESS('Comprehensive Mod Example loaded successfully!'))
