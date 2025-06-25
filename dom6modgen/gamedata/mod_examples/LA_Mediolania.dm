#modname "LA Nation: Mediolania, The Second Coming Current Version (v1.2) "
#icon "./mediolania/banner.png"
#description "Adds LA Mediolania, an Ermor successor nation of Catacomb Saints"
#version 1.2


-- fear -> dread ?? 

--==== v 1.23
-- FIX The assassination of priests during globals was checking for blood instead of holy
-- TWEAK Armatura Prophetae now gives +6 hp also (as other dom 6 armors)
-- TWEAK Holy shroud unique armor now also gives +10 hp

--==== v 1.23
-- TWEAK Holy Spirit Gained Recuperation, Fear 10->7
-- TWEAK Holy Undead loose the #noheal trait - you pay upkeep to keep them in good shape after all. Afflictions however need to be cured by caretaker nuns
-- TWEAK Holy Helper fear 10->7
-- FIX Hero Gaspar still had recuperation
-- CONTENT Updated Steam Banner

--==== v 1.22
-- FIX The paralyze weapons on Memento Mori and Charnels required hands, replaced those with an intrinsic paralysing attack 
-- FIX Memento Mori didn's have proper body type
-- FIX Charnel and Idolatrous Charnel had head butt attack as it wasn't immobile
-- FIX Battle Relic had head butt attack as it wasn't immobile 
-- FIX Found Saint had head butt attack as it wasn't immobile 

-- ===== v 1.21
-- TWEAK/FIX Pavise had absurd parry. Parry 14 -> 9, enc 4->5, rcost 3->4

-- ============ v 1.2 ===========================

-- Moved Monster IDs 8000 -> 10000 to prevent conflict with Sprite overhaul and Mormacil Mod Nations
-- FIX all grammar errors should hopefully be fixed now
-- FIX Heavenly Horn item had item id in illegal range (although there was no conflict ATM better fix this

 -- =========== v 1.13
 
 -- FIX Holy Choir and Choir leader did not work properly as communion slave / master
 -- FIX corrected bad grammar 
 -- FIX Gaspar, Melkir and Balthasar gained proper unit names

 -- =========== v 1.12 ============================================
 
 -- FIX Plead with Sepolte Vive was 1G 3H instead of 1B 3H
 -- FIX All the divine spells had Blood instead of Holy path
 -- FIX Description of dignitary saints was wrong 
 
 -- =========== v 1.11 ============================================
 
 -- removed #mounted tag 
 
--============= v 1.1 DOM6 RELEASE ================================
-- All Images now in PNG format
-- Sacred Medolanian undead lost recuperation and gained #noheal trait
-- Equite of the Second Coming gained skillrider 2, Destrier mount (3582 -- MA Mari Knight of the Chalice)
-- Centurion gcost 80 -> 110
-- Member of the ducal family gained skilledrider 1, Destreir Mount (3517), makemonsters1 -> makemonsters2, batstartsum2 -> batstartsum3, gcost 160->230
-- Monk gcost 45
-- Caretaker Nun lost diseasehealer 1, gained corpse stitcher 5. gcost 75 -> 100
-- Master Crafter gcost 190 -> 260
-- Bishop gcost 130 -> 180
-- Archbishop gcost 280 -> 390
-- Architect gcost 45 -> 60 (just copy of MA mari one still)
-- Battle Relic Gained 2 Bearer mounts (3585) and regainmount 1, hp 30, prot 15, pierce and slash res, mr 15, def 2, att 2, ap 2, no weapons
-- Bone Angel gained noheal lost recuperation
-- Found Sait gained 2 Bearer mounts (3585) and regainmount 1, hp 30, prot 7, pierce res, mr 15, def 2, att 2, ap 2, no weapons
-- Holy Helper multihero gained noheal lost recuperation
-- Added sacred Skeletal Camel mount for Gaspar 
-- Gaspar gained skeletal camel mount and regainmount 1, gained noheal lost recuperation
-- Balthasar gained Invulnerable 18 (he wears the kitharionic lion pelt), gained noheal lost recuperation
-- Heavenly Horn changed type to missile weapon, autorepeat Animate skeleton -> Animate Legionaire


--=============v 1.0=============================================== 

-- CONTENT Big sprite update
-- CONTENT Description Updates
-- CONTENT More names for catacomb saints
-- CONTENT Added futuresites to preview summons and heroes
-- CONTENT Monsters get proper unit ID, IDs referenced instead of names
-- CONTENT Pope prophet shape for Archbishops and Bishops, giving +1 H boost 
-- CONTENT Reanimation, Animate Skeleton, Raise Skeletons and Horde of Skeletons replaced with national version that includes ermorian longdead (50% of longdead will be ermorian)
-- CONTENT Added Days of Jugment global spell - dominion spawn longdead and angels attack enemy priests inside dominion
-- CONTENT Added Holy Chastisement - an H7 spell that strikes all enemy undead with holy fire, mr negates easily 
-- CONTENT H2 priests may now enter holy reliquary cap site to summon 1 catacomb martyr per turn
-- CONTENT Added Bone Archangel pretender
-- CONTENT Added Angel of Death pretender
-- CONTENT Added generic items - Vial of Martyr's blood, Martyr's Foot, Martyr's Head, Heart of a Martyr
-- CONTENT Added Holy Shround unique artifact  
-- TWEAK removed dashes from comments for better parsing  
-- TWEAK #wallmult for crosbow militia 15 > 10
-- TWEAK Crossbow militia leather cap to iron cap prec 10>9
-- TWEAk Pavise shield parry 9 to 10, def minus 2 to minus 4, prot 19 to 16, rcost 3, was missing previously
-- TWEAK Pavise crossbowman gcost 15>12 rpcost 19>15, iron cap > legionary helmet
-- TWEAK Battle pilgrim hp 9, undead pilgrim hp 5, rpcost 10>14
-- TWEAK Martyr Milite gains legionary helmet, gcost 40>20 (for upkeep sake)
-- TWEAK Equite rp 10000 > 58
-- TWEAK Centurion now fixed gcost 80, gains undead leadership 10
-- TWEAK Member of the Ducal Family rpcost 4 > 2, gcost 160 gains undead leadership 40
-- TWEAK Foot knight gained gcost 13 for upkeep
-- TWEAK Caretaker Nun gcost 65>75 rpcost 1, gains undead leadership 10
-- TWEAK Master Crafter E2 > E1, gcost 210 > 190
-- TWEAK Bishop now D1 H2 +1 FWSD, 130 gold, poorleader
-- TWEAK Archbishop gcost 380 > 280, gained magic staff instead of dagger, ok leader, atta and def 7 > 8, prec 7 > 10
-- TWEAK Catacomb martyr reworked, now with legionarry helmet and battleaxe, hp 13>9 def 12>11 att 13>11 prec 13>10, gcost 60 >28 (for upkeep)
-- TWEAK Capuchin Mummy gcost 20>8 (for upkeep), prot 5>8
-- TWEAK Catacomb Saints devided between Soldier Saints and Dignitary Saints
-- TWEAK Soldier Saints greatsword, full plate, legionary helmet, D1 H1 +1FWES +1FWES, awe 1, fear 5 
-- TWEAK Dignitary Saints dagger, robes, crown, D2 H2 +2FWES, awe 1
-- TWEAK Soldier saint 2 greatsword, plate cuirass, crown, D2 H1 +1FWES +1FWES, awe 1, combat caster
-- TWEAK summons gained poor leader instead of no leader mostly catacomb saints and human summons
-- TWEAK Capuchin brother +1 WD 25% > 100%
-- TWEAK Sepolta Viva +1 D 25% > 0%
-- TWEAK Bone Angel gains +1 D, looses chance at randoms, hp 45 > 35, gcost for upkeep 300>400
-- TWEAK Charnel doesn't increase order anymore, unrest reduction 1 > 5, bringer of fortune 1>3
-- TWEAK Idolatrus Charnel gold generation 40 > 20, bringer of fortune 4
-- TWEAK Charnel and Idolatrus Charnel paralyze attack 5 > 10
-- TWEAK Angel of Judgment A2 > A1 D3
-- TWEAK Holy helper multifhero - full plate mail > plate cuirass, fear 5 > 10
-- TWEAK Melkior Hero W2 > W1
-- TWEAK Prophet in White, cost 250, prot 0 >10, mr 20 > 18, mor 20>30, att,def 14 > 12, prec 13>12, fireres -10, awe 5 > 3, fear 5 > 10
-- TWEAK spell Consecrate Battle Relic D1H1 > D2H2, 20D gems to 15D gems, moved to enchantment
-- TWEAK spell Equip Catacomb Martyrs, split into 3 spells, all moved to enchantment
-- 	Baptize Catacomb Martyr -- D1H1, nreff 1, 2D gems, ench 2
-- 	Baptize Catacomb Centuria -- D2H2, nreff 8 + 1/2 per level, 14D gems, ench 4
-- 	Baptite Catacomb Cohort --D4H3, nreff 24, 32D gems, ench 6
-- TWEAK Consecrate catacomb martyr spell removed
-- TWEAK Equip Catacomb Saint > Canonize Catacomb Saint, moved to ench, 35Dgems > 30D gems
-- TWEAK Enchant Memento mori moved to construction, 2D gems to 3D gems, lvl3 to lvl2
-- TWEAK Construct Charnel const 5 > const 3
-- TWEAK Holy Bone Angel > Bone Angel Construction, moved to Construction lvl6 > lvl7
-- TWEAK Enchant Angel of the Choir > Channel Angel of the choir, moved to construction
-- TWEAK Enchant Angel of Judgment > Channel Angel of Judgment, moved to construction lvl5 > lvl6
-- TWEAK Commision Capuchin Friar > 15S gems to 21S gems
-- TWEAK Shepherd of Virgins > 21S to 22S gems
-- TWEAK Armatura Prophetae 3S2F > 2S2D 
-- TWEAK Heavenly Horn 2A > 2A1D, Autospell Raise skeletons > Raise Skeleton
-- TWEAK pretender selection looses neter of the underworld and lich queen, gains oracle, crone, great sage 
-- TWEAK defcom2 Bishop > Member of the Ducal Family
-- FIX Heroes not properly declared
-- FIX Nation color in graph was wrong, now properly purple
-- FIX Idolatrus Charnell was missing bringeroffortune
-- FIX Found Saint event commander had missing negative magic boosts, was a mage even before being transformed

--=================v 0.5 ===========================================

-- ADDED 3 Wise Men as unigue heroes:
--       * Melchior of Caelum
--       * Gaspar of Ind
--       * Balthasar of Machaka
-- ADDED summonable Angel of Judgment whose trumpet calls the dead
-- ADDED summonable Angel of the Choir communion slave like teurg communicant
-- ADDED Trumpet of Judgment national item Autocasts raise dead + Heavenly Horn attack
-- ADDED national rebate for "Flask of Holy Water" 
-- ADDED flavour events
--       * Catacombs and ruins of ancient empire can spawn catacomb saints to be brought to capital
--       * Charnel can transform to heretic + gold generation, purify with archbishop
-- ADDED Undead Repentance, H2 undead command with 20 range
-- ADDED Blessed be the Martyrs, H2 improved bless but only targets undead  
-- TWEAK 14 Holy Helpers multihero fear 3 > 5, corrected missing inanimate tag
-- TWEAK Catacomb Saint fear 3 > 5
-- TWEAK Charnel gets #bringeroffortune 1
-- TWEAK Prophet Shrouded in White D2S2 > D1S2
-- TWEAK Prophet Shrouded in White fixedname Jehoshua
-- TWEAK Protection of the Prophet removed fatigue cost
-- TWEAK Power of the Prophet removed fatigue cost
-- FIX Bone Angel mr 0 > 17
-- FIX big round of description updates and grammar correction 

--=========v 0.4 ========================================================
-- big sprite rework !
-- added missing attack sprites
-- revised a lot of sprites that were bad or just copies
-- sprites renamed for easier bookkeeping  

-- added Member of the Ducal Family commander
-- added Mediolanum Architect, same as MA Marignon Architect but with different name and description for flavour
-- added summonable Memento Mori flying skulls at ench 3, D2, 2 gems, 5+ units
-- added summonable Bone Angel commander
-- added summonable Charnel commander
-- added Prophet Shrouded in White as Pretender Chasis

-- added spell Protection of the Prophet, a H4, affect sacred only version of Protection of the Supeulchre without the mr negates easily
-- added spell Power of the Prophet, a H5 affect sacred only version of Power of the Sepulchre
-- added spell Holy Choir, an H2 version of communion slave
-- added spell Choir Leader, an H2 version of communion Master

-- added item "Armatura Prophetae" at const 6
-- added national rebate for "Shroud of the Battle Saint" item 

-- all undead saints and martyrs now mindless and lifeless. they follow what the people pray for
-- all undead saints and martyrs now cost upkeep. However they heal naturally and have recuperation as the faithful carefully tend to them
-- standard melee troop lineup changed to wear legionary helmets

-- Mediolanum Commander > Mediolanum Centurion, leadership 80, inspirational 1
-- Equite of the Second Coming gcost 65 > 50; rpcost 10000
-- Caretaker Nuns gain a 10% chance for an additional E or D path
-- Bishop gained 2F or 2S or 2D
-- Bishop and Archbishop gained Catacomb Saint Twiceborn shape
-- Capuchin Brother summons 2d6 mummies at start of battle
-- Mother Superior, master ritualist  minus 10 and mastersmith minus 10 to making blood items is bad ! Shame !

-- added #halfdeathinc and #halfdeathpop to the nation

--============v 0.35===================================
-- resized eddited sprites to proper size (64x64 or 128x128)
-- grammar and descprition changes /updates
-- pavise crossbow rp14 > rp 19

--==============v 0.3 =============================
-- added "Mother superior" > summonable blood hunter, with B1 but master ritualust minus 1
-- added spell to summon mother superior > Conj5 20 pearls
-- added "Sepolta viva" > D4 (up to D5) mage with a skull mentor that however requires a donation of 33 virgins to summon
-- removed crossbowman
-- added crossbow militia
-- added pavise crossbowman
-- removed mediolanum swordsman
-- added Ulmish greatsword, same equipment as mar. swordsman but ulmish stats
-- recoloured the Marignon troop lineup in glorious Mediolanum purple
-- Archbishop of the Second Coming mr 14 > 15
-- Master Crafter mr 11 > 14
-- Capuchin Borther WD 20% > WD 25%
-- Capuchin Brother makes 5 mummies instead of 2
-- Capuchin Mummy lost fire vulnerability
-- Catacomb Saint hp 17 > 23
-- holy helper hp 23 > 33
-- wall unit > crossbow militia
-- wall unit multiplier 10 > 15 

--===========v 0.2==================================
-- added capuchin brother + summoning spell
-- added Capuchin mummy, monsummon from capuchin brothers
-- added "consacrate catacomb martyr", weaker version of summon but castable at the site "Ruins of the Old Empire"
-- added Holy Helper Multihero
-- Fallen Pilgrim > sprite change to make more soullessy and diferent from pilgrim
-- Equite of the Second Coming > gcost 50 > 65, rpcost 46 > 50 (since better version of paladin, should cost slightly more)
-- Caretaker Nun E1 100% > E or D 50%

--========== To Do ==================================
-- add ritual to become patron saint, each fortress with temple gains empty saint spot, that can be filled by a catacomb saint, granting them (dominion)immortality and resetting home province 
-- DONE probably lower cumulative hp on pilgrims 
-- Pope prophet shape 
-- DONE reference ids instead of names, change names and descriptions
--  ADDED "Day of Judgment" spell, like howl but summons longdead ? (!!!!!!!!!!!!!!)
-- DONE add some events (ruins may spawn saint)
-- add ritual of rebirth version
-- DONE add twiceborn version ?
-- add more to prophet shrouded in white storyline
-- DONE ! add items
-- saints should have montag and different versions
-- * combat
-- * scholar
-- * priest
-- Summon Catacomb saint to spawn random saint
-- NOPE! Add equite of the Holy sepulcher, an undead sacred version of equite


-- Weapons

#newweapon 1708
#name "Golden Great Sword"
#magic
#dmg 10
#att 2
#def 3
#len 2
#nratt 1
#slash
#twohanded
#rcost 7
#end

#newweapon 1709
#copyweapon 282 -- paralyze 5 
#bonus 
#end

-- Armor

#newarmor 950
#name "Pavise"
#type 4
#prot 16
#def 4
#enc 5
#woodenarmor
#rcost 4
#end

-- UNITS


-- Crossbow Militia

#newmonster 10000
#spr1 "./mediolania/med_cros.png"
#spr2 "./mediolania/med_cros_2.png"
#name "Crossbow Militia"
#descr "Crossbows became increasingly popular in Mediolania and surrounding lands after they were introduced by the Marignese. With high availability and few training required, a contingent of crossbow militia can be quickly levied from the local populace. Although highly effective at providing a large volume of fire they have low morale and no training in hand to hand combat. The people of Mediolania are quite superstitious. They commonly wear a seven-knotted armband on the left hand for good luck. They also tie pieces of white cloth, drenched in their own blood to their weapons, so that they may strike true."
#weapon 25 -- crossbow
#weapon 9 -- dagger
#armor 6 -- ring mail cuiras
#armor 20 -- iron cap
#hp 10
#size 3
#mr 10
#mor 8
#str 10
#att 8
#def 8
#prec 9
#ap 12
#gcost 8
#rpcost 5
#end

-- Pavise Crossbowman

#newmonster 10001
#spr1 "./mediolania/cros_pavise.png"
#spr2 "./mediolania/cros_pavise_2.png"
#name "Pavise Crossbowman"
#descr "Crossbows became increasingly popular in Mediolania and surrounding lands after they were introduced by the Marignese. Professional crossbowmen began filling the ranks and  new tactics were developed. Being a professional crossbowman became a well paid and respectable job, and they are highly sought after. These elite crossbowmen use the pavise shield - a large, wooden, quickly deployable shield that offers excellent missile protection, but are quite cumbersome to use in melee. These shields are usually beautifully painted with motifs of the prophet's life. The people of Mediolania are quite superstitious. They commonly wear a seven-knotted armband on the left hand for good luck. They also tie pieces of white cloth, drenched in their own blood to their weapons, so that they may strike true."
#weapon 25 -- crossbow
#weapon 8 -- broad sword
#armor 9 -- plate cuirass
#armor 126 -- "Legionary Helmet"
#armor 950 --pavise
#hp 10
#size 3
#mr 10
#mor 12
#str 11
#att 10
#def 11
#prec 12
#ap 12
#gcost 12 
#rpcost 15 
#end

-- Pikeneer
#newmonster 10002
#spr1 "./mediolania/med_pike.png"
#spr2 "./mediolania/med_pike_2.png"
#copystats 221 -- MA mari Pike
#name "Mediolanum Pikeneer"
#descr "The Pikeneers of Mediolania take after their Marignese counterparts in terms of arms and armament. They wear Legionary helmets and armor decorated in the style of old Ermorian legions, when the Prophet shrouded in White performed his miracles. The people of Mediolania are quite superstitious. They commonly wear a seven-knotted armband on the left hand for good luck. They also tie pieces of white cloth, drenched in their own blood to their weapons, so that they may strike true."
#cleararmor
#armor 9 -- "Plate Cuirass"
#armor 126 -- "Legionary Helmet"
#end

-- Halberds 
#newmonster 10003
#spr1 "./mediolania/med_halb.png"
#spr2 "./mediolania/med_halb_2.png"
#copystats 220 -- MA mari Halb
#name "Mediolanum Halberdier"
#descr "The Halberdiers of Mediolania take after their Marignese counterparts in terms of arms and armament. They wear Legionary helmets and armor decorated in the style of old Ermorian legions, when the Prophet shrouded in White performed his miracles. The people of Mediolania are quite superstitious. They commonly wear a seven-knotted armband on the left hand for good luck. They also tie pieces of white cloth, drenched in their own blood to their weapons, so that they may strike true. Halberdiers are most commonly employed as guards and gain benefits in defending castles from sieges."
#cleararmor
#armor 9 -- "Plate Cuirass"
#armor 126 -- "Legionary Helmet"
#end

-- Swordsman 
#newmonster 10004
#spr1 "./mediolania/med_sword.png"
#spr2 "./mediolania/med_sword_2.png"
#copystats 1034 --LA Ulm Zweihander
#name "Ulmish Greatsword"
#descr "Ulm always had an eye on Mediolania for potential future expansion, even when under Marignon rule. This led to skirmishes, trade and an influx of Ulmish people. After the Malediction, there was a big wave of refugees. They mostly found work as smiths, crafters and soldiers. The ulmish greatswords fight in Ermorian style armor, much lighter than their Zweihander counterparts. They have stripes of Ulmish blue on their clothing to remember their heritage. The former inhabitants of Ulm are still large and can endure much physical punishment before collapsing, but are vulnerable to magic. The people of Mediolania are quite superstitious. They commonly wear a seven-knotted armband on the left hand for good luck. They also tie pieces of white cloth, drenched in their own blood to their weapons, so that they may strike true."
#cleararmor
#armor 9 -- "Plate Cuirass"
#armor 126 -- "Legionary Helmet"
#end

--Martyr
#newmonster 10005
#spr1 "./mediolania/med_marty.png"
#spr2 "./mediolania/med_marty_2.png"
#name "Martyr Milite"
#descr "The body of a pilgrim who sacrificed themselves in battle. They are adorned in fineries, armour and carry the blessing of the Prophet Shrouded in White. Their equipment mimics the armour they had in life, but is of much higher quality. The tower shields are exquisitely painted, usually depicting scenes of the Judgement Day. To keep the Martyr in acceptable conditions some upkeep needs to be paid each month."
#weapon 1 -- "Spear"
#armor 19 --"Full Plate Mail" 
#armor 126 -- "Legionary Helmet"
#armor 4 --"Tower Shield" 
#hp 7
#size 3
#mr 12
#mor 50
#str 12
#def 11
#att 11
#prec 11
#ap 14
#mapmove 21
#enc 0
#coldres 15
#poisonres 25
#pooramphibian
#pierceres
#undead
#inanimate
#neednoteat
--#heal
--#noheal
#spiritsight
#holy
#gcost 20 -- for upkeep 
#end

--Undead Pilgrim 
#newmonster 10006
#spr1 "./mediolania/fallen_pilgrim.png"
#spr2 "./mediolania/fallen_pilgrim_2.png"
#name "Fallen Pilgrim"
#descr "A pilgrim who was given a second chance by the divine intervention of the Prophet Shrouded in White. Should his body survive the battle he will be proclaimed a martyr, holy to the people of Mediolania and dressed in gilded armor and fineries." 
#weapon 1 -- "Spear" 
#armor 32 -- "Rusty Ring Mail Hauberk"  
#armor 126 -- "Legionary Helmet"
#armor 170 -- "Rotten Tower Shield"  
#hp 5
#size 3
#mr 10
#mor 50
#str 10
#def 8
#att 8
#prec 8
#ap 8
#mapmove 21
#enc 0
#coldres 15
#poisonres 25
#pooramphibian
#pierceres
#undead
#inanimate
#neednoteat
--#noheal
#spiritsight
#firstshape 10005 -- "Martyr Milite"
#end

-- Battle Pilgrim
#newmonster 10007
#spr1 "./mediolania/battle_pilgrim.png"
#spr2 "./mediolania/battle_pilgrim_2.png"
#name "Mediolanum Pilgrim"
#descr "It is mandatory for every citizen of Mediolania to do a pilgrimage to Eldergate through the wasteland surrounding it. Along the way they collect many artefacts and weapons from the old empire. Brought back to Mediolania, these artefacts are considered sacred. In time of war, these pilgrims join the armies as Miles Propheta - the soldiers of the Prophet. The Prophet shrouded in white will give another chance to his soldiers should they fall in battle. If the body of the fallen soldier survives the battle he will be proclaimed a martyr, holy to the people of Mediolania and dressed in gilded armor and fineries. Pilgrims have good morale, and slightly higher magic resistance and strength due to their travails in Ermorian lands. The people of Mediolania are quite superstitious. They commonly wear a seven-knotted armband on the left hand for good luck. They also tie pieces of white cloth, drenched in their own blood to their weapons, so that they may strike true."  
#weapon 1 -- "Spear"
#armor 32 -- "Rusty Ring Mail Hauberk"  
#armor 126 -- "Legionary Helmet"
#armor 170 -- "Rotten Tower Shield"  
#hp 9
#size 3
#mr 11
#mor 13
#str 12
#def 9
#att 9
#prec 9
#ap 11
#mapmove 14
#enc 3
#gcost 10
#rpcost 14 --10
#secondshape 10006 --"Fallen Pilgrim"
#end

-- Equite of the Second Coming 
#newmonster 10008
#spr1 "./mediolania/eq_sec_coming.png"
#spr2 "./mediolania/eq_sec_coming_2.png"
#unmountedspr1 "./mediolania/eq_sec_coming_unm.png"
#unmountedspr2 "./mediolania/eq_sec_coming_unm_2.png"
#copystats 135 --Knight of the Chalice
#name "Equite of the Second Coming"
#descr "The Equites of the Second Coming are a holy order of knights dedicated to protecting the earthly church of the Prophet Shrouded in White and its dignitaries. Evolved from the Marignon knightly school, they have been granted ancient replicas of the white shroud. Found all over Ermorian lands, these shrouds have been cleaned with wine and purified in special ceremonies. The shrouds give them surprising healing powers. Although sacred status in Mediolania is usually reserved only for Martyrs and high church officials, as protectors of the earthly church, they are deemed holy."
#mountmnr 3582 -- MA Mari Knight of the Chalice destrier
--#skilledrider 2
#heal
#def 12
#bodyguard 2
#gcost 50
#rpcost 58
#end

--Foot Knight
#newmonster 10009
#spr1 "./mediolania/foot_knight.png"
#spr2 "./mediolania/foot_knight_2.png"
#name "Foot Knight"
#descr "As in most lands, nobles often join a knightly order and form an elite fighting force. However due to the devastation of Ermor, horses are scarce in Mediolania and reserved only for the members of the Ducal family and the sacred order of the Equites. Thus Mediolanian knights fight on foot, eager to prove themselves worthy and perhaps get adopted into the Ducal family, thus receiving higher status and better training. They often accompany members of the Ducal family to show them their valour in person."
#weapon 8 -- "Broad Sword"
#armor 18 -- "Full Chain Mail"
#armor 126 -- "Legionary Helmet"
#armor 3 --"Kite Shield"
#hp 12
#size 3
#prot 0
#mr 10
#mor 13
#str 11
#att 11
#def 11
#prec 10
#ap 12
#mapmove 16
#enc 2
#startage 22
#maxage 50
#humanoid
#gcost 13
#end



-- COMMANDERS

--default scout

#newmonster 10050
#spr1 "./mediolania/med_cap.png"
#spr2 "./mediolania/med_cap_2.png"
#name "Mediolanum Centurion"
#descr "The commanders of Mediolania imitate the centurions of old Ermor, when the Prophet shrouded in white performed his miracles. They wear replicas of the sacred shroud which inspires the troops to great feats of bravery and religious zeal. These shrouds are seldom blessed however, and don't provide the healing powers of consecrated shrouds."
#nametype 114 --Marignon man
#armor 9 -- "Plate Cuirass"
#armor 126 -- "Legionary Helmet"
#weapon 8 -- "Broad Sword"
#hp 12
#size 3
#prot 0
#mr 10
#mor 12
#str 10
#att 11
#def 12
#prec 10
#ap 12
#mapmove 20
#enc 3
#startage 22
#maxage 50
#goodleader
#poorundeadleader
#inspirational 1
#humanoid
#gcost 110 --80
#rpcost 1
#end

#newmonster 10051
#spr1 "./mediolania/ducal_family.png"
#spr2 "./mediolania/ducal_family_2.png"
#unmountedspr1 "./mediolania/ducal_family_unm.png"
#unmountedspr2 "./mediolania/ducal_family_unm_2.png"
#name "Member of the Ducal Family"
#descr "Officially Mediolania is governed by the Dux or Duke, although real authority lies with the Archbishops. Still the Duke and his extended family are considered in high regard by the commoners of Mediolania and the leadership of most day to day secular matters as well as matters of warfare are left to them. The members of the extended family carry the replica of the Shroud in battle, greatly improving the morale of the troops they command and driving them to great feats of Zeal. The replica of the Shroud is blessed by the Archbishops to gain favour from the ruling family and therefore also grands healing power to the bearer. The Archbishops also gave them authority to command a small number of the sacred dead. When not commanding armies they can attract minor nobles eager to impress them and get adopted into the Ducal family. They are likewise always accompanied in battle by three of their favourite nobles."
#nametype 114
#weapon 8 -- "Broad Sword"
#armor 18 -- "Full Chain Mail"
#armor 126 -- "Legionary Helmet"
#armor 3 --"Kite Shield"
#mountmnr 3517 -- Destrier
#skilledrider 1
#hp 16
#size 3
#prot 0
#mr 11
#mor 15
#str 13
#att 14
#def 14
#prec 11
#ap 18
#mapmove 22
#enc 4
#startage 22
#maxage 50
#expertleader
#okundeadleader
#batstartsum3 10009 --"Foot Knight"
#makemonsters2 10009 --"Foot Knight"
#heal
#inspirational 2
#humanoid
#gcost 230 --160
#rpcost 2
#end


#newmonster 10052
#spr1 "./mediolania/monk.png"
#spr2 "./mediolania/monk_2.png"
#copystats 60
#name "Mediolanum Monk"
#descr "Monks live in monasteries all over Mediolania. They pray, copy and study the holy scriptures. They can be used to help research when in the dominion of the True God. As they are guided by divine insight, only a certain number of them, equal to the strength of the Dominion, may research in the same province."
#nametype 114 --Marignon man
#gcost 45
#end


#newmonster 10053
#copyspr 2249 --Nun
#copystats 1438 -- LA aga Ktonian necromancer
#name "Caretaker Nun"
#descr "Nuns are members of various convents. They are in charge of decorating and repairing the undead saints and martyrs of Mediolania. They often accompany the armies of Mediolania, but not to heal the living, but rather the holy dead. They may have some knowledge in the magic of death or earth."
#nametype 118 --Pythium Female
#clearweapons
#clearmagic
#weapon 92
#custommagic 5120 50 -- 0.5 ED
#custommagic 5120 10 -- 0.1 ED
#magicskill 9 1 -- H1
#darkvision 0
#female
#noslowrec
#gcost 100
#rpcost 1
#poorundeadleader
#end



#newmonster 10054
#spr1 "./mediolania/med_crafter.png"
#spr2 "./mediolania/med_crafter_2.png"
#name "Master Crafter"
#descr "Master crafters are in charge of producing the ornaments that adorn the reliquaries and the martyrs, as well as producing the intricate armor and weapons for the Martyr Milite - the army of the Martyrs. Most of them came as refugees from Ulm after the Malediction, but Mediolania already had respectable Craftsmen of its own. By the sharing of knowledge between the two groups, these crafters might even supersede the smiths of the golden era of Ulm."
#nametype 114 --Marignon man
#weapon "Hammer"
#hp 12
#size 3
#mr 14
#mor 10
#str 10
#att 8
#def 8
#prec 8
#ap 12
#mastersmith 1
#magicskill 3 1 --E
#magicskill 0 1 --F
#magicskill 4 1 --S
#poorleader
#startage 30
#maxage 50
#gcost 260 -190
#rpcost 2
#humanoid
#end


#newmonster 10055
#spr1 "./mediolania/bishop.png"
#spr2 "./mediolania/bishop_2.png"
#copystats 1647 -- LA Man bishop
#name "Mediolanum Bishop"
#descr "The Bishops of Mediolanum are high ranking dignitaries of the Church of the Second Coming. They lead congregations and prayers, and look after the bodies and reliquaries of the martyrs. In times of war they are given the authority to lead the Armies of Martyrs into battle."
#nametype 114 --Marignon man
#okundeadleader
#magicskill 5 1 -- D1
#custommagic 6784 100 --+1FWSD
#startage 30
#maxage 50
#poorleader
#gcost 180 --130
#rpcost 2
#twiceborn 10060 --"Dignitary Saint"
#prophetshape 10074 --Pope
#end


#newmonster 10056
#spr1 "./mediolania/archbishop.png"
#spr2 "./mediolania/archbishop_2.png"
#name "Archbishop of the Second Coming"
#descr "The Archbishops of the Second Coming are the highest dignitaries of the Church. It is them who perform the rights of martyrdom, sanctify and resurrect the heavenly bodies of the Martyrs and the Catacomb Saints. A fact only known to them is that the Saints and Martyrs as well as the promised afterlife, can only be achieved through the prayers, faith and will of the people. They keep this secret well, lest the pillars of Mediolania crumble."
#nametype 114 --Marignon man
#weapon 238 -- magic staff
#armor 158 --robes
#hp 10
#size 3
#mr 15
#mor 12
#str 8
#att 8
#def 8
#prec 10
#ap 10
#holy
#magicskill 5 2 --D 2
#magicskill 4 1 --S 1
#magicskill 0 2 --F 2
#magicskill 9 3 --H 3
#custommagic 6784 10 --10% F,W,S,D
#startage 40
#maxage 50
#okleader
#gcost 390 --280
#rpcost 4
#twiceborn 10060 --"Catacomb Saint"
#prophetshape 10074 --Pope
#humanoid
#end

#newmonster 10057
#copyspr 3010 --MA mari arch
#copystats 3010
#name "Mediolanum Architect"
#descr "As with craft, architecture has prospered in Mediolania. The architects of Mediolanum build wondrous temples and cathedrals, including the magnificent Cathedral of the Second Coming. Their expertise is not limited only to temples, however. They can construct more advanced fortifications and help when defending or besieging castles."
#end


-- SUMMONED UNITS

-- Catacomb Martyr
#newmonster 10010
#spr1 "./mediolania/catacomb_martyr.png"
#spr2 "./mediolania/catacomb_martyr_2.png"
#name "Catacomb Martyr"
#descr "One of the holy skeletons of ancient Martyrs, brought from Eldergate and interred in the Holy Reliquary. There are many thousands of unnamed Martyrs in the reliquary, and, although not worshipped as the named saints, they are still sacred and held in high regard. In times of need these holy martyrs are decorated in jewels and dressed in fine gilded armor. As Milites Propheta - the warriors of the prophet, they rise to do battle against the unfaithful. The beautiful jewels and armor are said to awe opponents. To keep the Martyr in acceptable conditions some upkeep needs to be paid each month."
#weapon 18 -- BATTLEAXE 
#armor 19 --"Full Plate Mail"  
#armor 126 -- "Legionary Helmet"
#hp 9--13
#size 3
#mr 12
#mor 50
#str 12
#def 11 --12
#att 11 --13
#prec 10 --13
#ap 13
#mapmove 21
#enc 0
#coldres 15
#poisonres 25
#pooramphibian
#pierceres
#undead
#inanimate
#neednoteat
--#heal
--#noheal
#spiritsight
#holy
#gcost 28
#awe 1
#end


-- Capuchin Mummy
#newmonster 10011
#spr1 "./mediolania/cap_mummy.png"
#spr2 "./mediolania/cap_mummy_2.png"
#name "Capuchin Mummy"
#descr "A mummy made by the Capuchins and given a simple broadsword. These mummies have tough leathery bodies and can serve to bolster frontline troops. Unlike mummies made by fouler rituals, they don't spread disease or leprosy, and are not vulnerable to fire. The mummies are mostly commoners and therefore are not sacred. The Capuchins require a monthly fee for each mummy however, so care needs to be taken not to overspend."
#weapon 8 --"Broad Sword"
#hp 30
#size 3
#prot 8
#gcost 8
#mr 10
#mor 50
#str 15
#att 11
#def 7
#prec 8
#ap 8
#mapmove 22
#enc 0
#undead
#inanimate
#neednoteat
#spiritsight
#coldres 15
#poisonres 25
#noheal
#end

-- Flying Skulls !!
#newmonster 10012
#spr1 "./mediolania/mem_mori.png"
#spr2 "./mediolania/mem_mori_2.png"
#name "Memento Mori"
#descr "The Memento Mori are enchanted human skulls with raven wings. They are used by the Church to keep the populace placated by whispering of their eventual death and demise, and the glory that awaits those pious enough when the Prophet Shrouded in White returns. During times of war they can be employed to harass enemies, paralysing them with whispers and visions of death."
#weapon 1709 --"Paralyze (5)"
#hp 2
#size 1
#prot 0
#mor 50
#mr 9
#str 4
#att 10
#def 18
#prec 7
#ap 4
#mapmove 22
#enc 0
#undead
#inanimate
#neednoteat
#spiritsight
#coldres 15
#poisonres 25
--#fear 1
#incunrest -1 --0.1 per month
#flying
#noheal
#bird
#end

#newmonster 10013
#spr1 "./mediolania/choir_angel.png"
#spr2 "./mediolania/choir_angel_2.png"
#name "Angel of the Choir"
#descr "Angels of the Choir are holy bones of martyrs fashioned in the shape of a minor Angel and believed to be inhabited by an Angel of the Choir of the True God. The Angel of the Choir sings divine songs and automatically joins communions as a communion slave while on the battlefield. It has angelic attributes such as awe and invulnerability to mundane weapons since the people believe it has."
#weapon 92 --fist
#hp 16
#size 5
#prot 0
#mr 16
#mor 50
#noleader
#goodundeadleader
#str 11
#att 12
#def 12
#prec 12
#ap 16
#mapmove 34
#startage 250
#maxage 900
#enc 0
#flying
#holy
#undead
#inanimate
#mind
#neednoteat
#spiritsight
#pierceres
#coldres 15
#poisonres 25
#fireres 5
#shockres 5
#awe 5
#invulnerable 15
#magicbeing
--#heal
--#noheal
#gcost 100
#comslave
#end

#newmonster 10014
#copystats 187 -- Longdead legionnaire
#copyspr 187 -- Longdead legionnaire
#montag 6661
#end

#newmonster 10015
#copystats 186 -- Longdead velite
#copyspr 186 -- Longdead velite
#montag 6661
#end

#newmonster 10016
#copystats 1657 -- Longdead triarius
#copyspr 1657 -- Longdead triarius
#montag 6661
#end

#newmonster 10017
#copystats 1658 -- Longdead principe
#copyspr 1657 -- Longdead principe
#montag 6661
#end

#newmonster 10018
#copystats 196 -- Longdead spear naked
#copyspr 196 -- Longdead spear naked
#montag 6661
#end

#newmonster 10019
#copystats 195 -- Longdead spear
#copyspr 195 -- Longdead spear
#montag 6661
#end

#newmonster 10020
#copystats 194 -- Longdead sword naked
#copyspr 194 -- Longdead sword naked
#montag 6661
#end

#newmonster 10021
#copystats 192  -- Longdead sword
#copyspr 192 -- Longdead sword
#montag 6661
#end


-- SUMMONED COMMANDERS

-- Battle Relic
#newmonster 10058
#spr1 "./mediolania/battle_reliquary.png"
#spr2 "./mediolania/battle_reliquary_2.png"
#unmountedspr1 "./mediolania/br_unm.png"
#unmountedspr2 "./mediolania/br_unm.png"
#name "Battle Relic"
#descr "A consecrated relic carried to battle to inspire the faithful. It will drive the armies of Mediolania to new feats of bravery. Such consecrated Relics usually draw pilgrims to them when inside God's Dominion. Should one of the bearers be slain in battle, another pilgrim will immediately take their place."
#nametype 288 -- custom list of real catacomb saints
--#weapon 346 -- useless kick
#immobile
#nofmounts 2
#mountmnr 3585 -- bearer
#regainmount 1
#hp 30
#prot 15
#pierceres
#slashres
#size 4
#mr 15
#mor 50
#str 2
#att 2
#def 2
#prec 5
#ap 2
#holy
#poorleader
#itemslots 786432 -- 2 misc
#onebattlespell 242 --"Fanaticism"
#domsummon2 10007 --"Mediolanum Pilgrim"
#magicskill 9 1
#end


--Catacomb Saint Soldier
#newmonster 10059
#spr1 "./mediolania/catacomb_saint_pancratius.png"
#spr2 "./mediolania/catacomb_saint_pancratius_2.png"
#name "Soldier Saint"
#descr "The Bones of named Saints are held in particularly high regard. These sanctified martyrs are usually divided into three main categories - soldier saints, high dignitaries, and hierophant saints. Warrior Saints are adorned with the best jewelled armor and weapons. They don't have the priestly or magical power of the high dignitaries or hierophant saints but have the best martial prowess. Enemies of the prophet flee before the soldier saints and don't dare strike them for fear of divine punishment. The truth is that the Saints behave as the people believe they would. To keep the Saint in acceptable conditions some upkeep needs to be paid each month."
#nametype 288 --custom list of real catacomb saints
#weapon 11 --greatsword
#armor 19 --Full Plate Mail
#armor 126 -- "Legionary Helmet"
#hp 23
#size 3
#mr 13
#mor 50
#str 15
#def 12
#att 12
#prec 11
#ap 12
#mapmove 21
#enc 0
#coldres 15
#poisonres 25
#pooramphibian
#pierceres
#magicskill 5 1
#magicskill 9 1
#custommagic 3712 100 -- +1 FWES
#custommagic 3712 100 -- +1 FWES
#undead
#inanimate
#neednoteat
#mind 
--#noheal
#spiritsight
#holy
#awe 1
#fear 5
#poorleader
#goodundeadleader
#gcost 240 --for upkeep
#montag 6660
#end

--Catacomb Saint dignitary 
#newmonster 10060
#spr1 "./mediolania/catacomb_saint_konstantinus.png"
#spr2 "./mediolania/catacomb_saint_konstantinus_2.png"
#name "Dignitary Saint"
#descr "The Bones of named Saints are held in particularly high regard. These sanctified martyrs are usually divided into three main categories - soldier saints, high dignitaries, and hierophant saints. High Dignitaries are those highly learned in magic and the holy arts. They don't have the martial prowess of soldier or hierophant saints but they make up for it in priestly and magical powers. Enemies of the prophet flee before the soldier saints and don't dare strike them for fear of divine punishment. The truth is that the Saints behave as the people believe they would. To keep the Saint in acceptable conditions some upkeep needs to be paid each month."
#nametype 288 --custom list of real catacomb saints
#weapon 9 --dagger
#armor 158 -- robes
#armor 148 -- crown 
#hp 15
#size 3
#mr 15
#mor 50
#str 10
#def 10
#att 10
#prec 11
#ap 12
#mapmove 21
#enc 0
#coldres 15
#poisonres 25
#pooramphibian
#pierceres
#magicskill 5 2 -- D2
#magicskill 4 1 -- S1
#magicskill 9 2 -- H2
#custommagic 3712 200 -- +2 FWES
#undead
#inanimate
#neednoteat
#mind 
--#noheal
#spiritsight
#holy
#awe 1
#poorleader
#goodundeadleader
#gcost 240 --for upkeep
#montag 6660
#end

#newmonster 10061
#spr1 "./mediolania/catacomb_saint_deodatus.png"
#spr2 "./mediolania/catacomb_saint_deodatus_2.png"
#name "Hierophant Saint"
#descr "The Bones of named Saints are held in particularly high regard. These sanctified martyrs are usually divided into three main categories - soldier saints, high dignitaries, and hierophant saints. Hierophant Saints perform their miracles and powerful magic on the battlefield, being both warriors and mages. They don't have the priestly or magical power of the high dignitaries but have superior martial prowess. Enemies of the prophet flee before the soldier saints and don't dare strike them for fear of divine punishment. The truth is that the Saints behave as the people believe they would. To keep the Saint in acceptable conditions some upkeep needs to be paid each month."
#nametype 288 --custom list of real catacomb saints
#weapon 11 --greatsword
#armor 9 -- "Plate Cuirass"
#armor 148 -- crown 
#hp 23
#size 3
#mr 13
#mor 50
#str 15
#def 12
#att 12
#prec 11
#ap 12
#mapmove 21
#enc 0
#coldres 15
#poisonres 25
#pooramphibian
#pierceres
#magicskill 5 2
#magicskill 9 1
#custommagic 3712 100 -- +1 FWES
#custommagic 3712 100 -- +1 SFWES
#undead
#inanimate
#neednoteat
#mind 
--#noheal
#spiritsight
#holy
#awe 1
#combatcaster
#poorleader
#goodundeadleader
#gcost 240 --for upkeep
#montag 6660
#end


-- Capuchin --
#newmonster 10062
#spr1 "./mediolania/capucin.png"
#spr2 "./mediolania/capucin_2.png"
#name "Capuchin Brother"
#descr "The Order of the Friars Minor Capuchin are known for their elaborate ossuaries and crypts. Over the years they have perfected the art of mummification. By placing a body on a grate over running water, the body is dehydrated. It is subsequently pickled by covering it in vinegar and left to dry in the sun. Many rich families flock to the Capuchins to have their bodies mummified after death. Vowed to poverty, the Capuchins are happy to oblige those seeking mummification... for a small donation to their order and a yearly fee. They also bring a squad of mummies to battlefields for protection."
#nametype 114 --Marignon man
#weapon 9 --dagger
#hp 9
#size 3
#mr 11
#mor 12
#poorleader
#holy
#str 9
#att 8
#def 8
#prec 9
#ap 10
#magicskill 2 1
#magicskill 5 1
#magicskill 9 1
#custommagic 4608 100 -- W or D
#makemonsters5 10011 --"Capuchin Mummy"
#batstartsum2d6 10011 --"Capuchin Mummy"
#end


-- Mother Superior
#newmonster 10063
#spr1 "./mediolania/med_mot_sup.png"
#spr2 "./mediolania/med_mot_sup_2.png"
#name "Mother Superior"
#descr "A Mother Superior of one of the numerous orders of nuns. Once a nun reaches this rank she is given the task to wander through the towns and villages of Mediolania in search for virgins to join the convent. Virgins are preferred as their purity reflects the pure white of the Prophet's Shroud. Through years of practice they have become quite efficient at their job, able to detect those of pure blood more easily. As an unfortunate side effect, they also gained rudimentary understanding of the power of blood. Though they are strictly forbidden by earthly and heavenly law to practice the foul blood magic, they may resort to its use if caught on the field of battle for self defence - a practice reluctantly condoned by the Church."
#nametype 118 --Pythium Female
#weapon 9 --dagger
#hp 9
#size 3
#mr 13
#mor 12
#poorleader
#holy
#str 8
#att 8
#def 7
#prec 7
#ap 9
#startage 40
#older 10 -- makes it old age
#maxage 50
#female
#magicskill 8 1
#magicskill 9 2
#douse 1
#masterrit -10
#mastersmith -10
#end


--Sepolta viva
#newmonster 10064
#spr1 "./mediolania/med_sv.png"
#spr2 "./mediolania/med_sv_2.png"
#name "Sepolta Viva"
#descr "The Nun order of the Sepolte Vive - meaning buried alive, takes corporal mortification and morbidity to the extreme. They sleep in coffins, inside ossuaries decorated with the bones of former nuns. If one of them dies they are not buried, instead they are left where they died so that others might contemplate mortality and see the decay of the earthly body. This environment attunes the sisters to death magic more so than anybody else in Mediolania. They often carry a skull of former mentors or friends. The skull is said to whisper secrets from beyond the grave to those willing to listen."
#nametype 118 --Pythium Female
#weapon 9 --dagger
#hp 9
#size 3
#mr 15
#mor 15
#poorleader
#holy
#str 9
#att 9
#def 9
#prec 10
#ap 10
#female
#magicskill 5 4
#magicskill 8 1
#startitem 374 --"Skull Mentor"
#end

-- Bone Angel --
#newmonster 10065
#spr1 "./mediolania/bone_angel.png"
#spr2 "./mediolania/bone_angel_2.png"
#name "Bone Angel"
#descr "The Bone Angel is the body of a Saint with wings made of bones belonging to high standing bishops of the past and feathers of ravens. They are usually given no armor, instead being wrapped in a replica of the Shroud, indicating the very high stature of the Angel. It is also equipped with an exquisitely crafted golden greatsword. As with other saints and martyrs it is the will and prayers of the believers that give it life and purpose. As the people believe it is an angel, it has many of the angelic attributes, such as being invulnerable to mundane weapons and celestial awe. In addition it brings the realisation of mortality to enemies making them cower in fear."
#armor 158 -- robes
#armor 148 -- crown 
#weapon 1708 -- "Golden Greatsword"
#hp 35
#size 6
#ressize 5
#prot 0
#mr 17
#mor 50
#poorleader
#goodundeadleader
#str 14
#att 14
#def 14
#prec 13
#ap 16
#mapmove 22
#startage 250
#maxage 900
#enc 0
#magicskill 0 2 --F2
#magicskill 1 2 --A2
#magicskill 4 2 --S2
#magicskill 5 1 --D1
#magicskill 9 3 --H3
#awe 5
#fear 5
#invulnerable 25
#flying
#holy
#undead
#inanimate
#neednoteat
#spiritsight
#pierceres
#coldres 15
#poisonres 25
#fireres 5
#schockres 5
#magicbeing
--#noheal
#gcost 400
#end


--Charnel
#newmonster 10066
#spr1 "./mediolania/charnel.png"
#spr2 "./mediolania/charnel_2.png"
#name "Charnel"
#descr "The bones and especially skulls of the faithful commoners of Mediolania are used to create Charnels. Charnels spread the dominion of the True God. The people gather around Charnels to contemplate mortality and the region where the charnel is located will become more peaceful. Acting as a conduit of worship, the True God may gift the populace with good events. It has some priestly authority and is sacred to the people of Mediolania. In battle it will fill the hearts of the unbelievers which come close with the dread of mortality, paralyzing them. People may start attributing miracles to the bones in the charnel instead of the True God, bringing offerings of gold. The charnel may then transform into a heretical version and will need to be purified by an Archbishop."
#weapon 1709 --"Paralyze" 10
#miscshape
#hp 35
#size 5
#prot 5
#mr 14
#noleader
#poorundeadleader
#mor 50
#str 0
#att 0
#def 0
#prec 11
#ap 1
#mapmove 0
#startage 55
#maxage 500
#holy
#undead
#inanimate
#neednoteat
#spiritsight
#pierceres
#coldres 15
#poisonres 25
#fear 5
#spreaddom 1
#incunrest -50 --5
--#decscale 0 --increases Order
#bringeroffortune 3
#magicskill 9 1
--#autospell "Smite"
--#autospellrepeat 1
#immobile
#end

-- Idolatrous Charnel
#newmonster 10067
#spr1 "./mediolania/id_charnel.png"
#spr2 "./mediolania/id_charnel_2.png"
#name "Idolatrous Charnel"
#descr "The bones and especially skulls of the faithful commoners of Mediolania are used to create Charnels. Charnels usually spread the dominion of the True God. However, sometimes the populace will start to worship the skulls in the Charnel instead of using the Charnel as a conduit to the Awakening God. Certain skulls will be attributed magical powers and be proclaimed bringers of luck. This decreases the dominion of the God in the province as the people turn to idolatry. On the positive side, people will offer gifts of gold and valuables which may be collected to fund the Church of the Prophet. The worship will also increase the number of good events somewhat. Only an Archbishop may purify the charnel and turn people away from idolatry."
#weapon 1709 --"Paralyze" 10
#miscshape
#hp 35
#size 5
#prot 5
#mr 14
#noleader
#poorundeadleader
#mor 50
#str 0
#att 0
#def 0
#prec 11
#ap 1
#mapmove 0
#startage 55
#maxage 500
#holy
#undead
#inanimate
#neednoteat
#spiritsight
#pierceres
#coldres 15
#poisonres 25
#fear 5
#heretic 3
#gold 20
#bringeroffortune 4
--#spreaddom 1
--#incunrest -10
--#decscale 0 --increases Order
#magicskill 8 1
--#autospell "Smite"
--#autospellrepeat 1
#immobile
#end

-- Angel of Judgment
#newmonster 10068
#spr1 "./mediolania/judgment_angel.png"
#spr2 "./mediolania/judgment_angel_2.png"
#name "Angel of Judgment"
#descr "Angels of Judgment are holy bones of Saints fashioned in the shape of an Angel and believed to be inhabited by an Angel of the True God. The Angel of Judgment uses its trumpet to awaken the dead and call them forth to be judged. The faithful dead shall rise to help the forces of Mediolania, while the heretic undead shall be burned and destroyed by the trumpet."
--#weapon 145 --heavenly horn
#weapon 92 --fist
#hp 25
#size 6
#ressize 5
#prot 0
#mr 16
#mor 50
#noleader
#goodundeadleader
#str 11
#att 12
#def 12
#prec 12
#ap 16
#mapmove 34
#startage 250
#maxage 900
#enc 0
#magicskill 1 1
#magicskill 5 3
#magicskill 8 2
#flying
#holy
#undead
#inanimate
#mind
#neednoteat
#spiritsight
#pierceres
#coldres 15
#poisonres 25
#fireres 5
#shockres 5
#awe 5
#invulnerable 15
#magicbeing
--#noheal
#startitem 740 --Heavenly horn
#gcost 150
#end


-- Found Saint --
#newmonster 10069
#spr1 "./mediolania/found_saint.png"
#spr2 "./mediolania/found_saint_2.png"
#unmountedspr1 "./mediolania/fs_unm.png"
#unmountedspr2 "./mediolania/fs_unm.png"
#name "Found Saint"
#descr "The remnants of a Saint found in the ruined catacombs of the Old Empire! It must be transported to the Holy Reliquary to be cleansed, rebaptised and equipped. Should one of the bearers be slain in battle, another pilgrim will immediately take their place."
#nametype 288 -- custom list of real catacomb saints
#weapon 346 -- useless kick
#nofmounts 2
#mountmnr 3585 -- bearer
#regainmount 1
#immobile
#hp 30
#size 4
#prot 7
#pierceres
#mr 15
#mor 50
#str 2
#att 2
#def 2
#prec 5
#ap 2
#holy
#poorleader
#itemslots 786432 -- 2 misc
#onebattlespell 242 --"Fanaticism"
#magicskill 5 2
#magicskill 9 2
#custommagic 3712 100 -- +1 FWES
#custommagic 3712 100 -- +1 FWES
#magicboost 0 -5 -- F
#magicboost 2 -5 -- W
#magicboost 3 -5 -- E
#magicboost 4 -5 -- S
#magicboost 5 -5 --D
#end


------- HEROES

--14 Holy Helpers

#newmonster 10070
#spr1 "./mediolania/holy_helper.png"
#spr2 "./mediolania/holy_helper_2.png"
#name "Holy Helper"
#descr "One of the Fourteen Holy Helpers, patron saints invoked against the plague and similar diseases. They died serving the Prophet Shrouded in White by helping the poor affected by plague. Now with the grace of the Prophet they have returned once more to help the faithful. Their magical scythes absorb diseases from the faithful and transform part of the diseases and suffering into death gems. The other part is stored and unleashed on the battlefield against the enemies of the Prophet. They are dressed completely in black to represent the black death, with a beautifully jewelled gilded breastplate. They wear a laurel crown symbolising their victory over death. Different Helpers have different magic skills. As bringers of death, they are greatly feared among the enemies of the True God." 
#weapon 506 --"Plague Scythe"
#armor 9 -- plate cuirass
#armor 148 -- crown 
#hp 33
#size 3
#mr 17
#mor 50
#str 14
#def 13
#att 12
#prec 12
#ap 12
#mapmove 21
#enc 0
#coldres 15
#poisonres 25
#pooramphibian
#pierceres
#magicskill 5 3
#magicskill 9 2
#custommagic 896 200 --+2FAW
#undead
#neednoteat
--#noheal
#spiritsight
#holy
#awe 2
#fear 7
#goodundeadleader
#autodisgrinder 1
#gcost 280
#inanimate
#end

-- Melchior of Caelum
#newmonster 10071
#spr1 "./mediolania/melchior.png"
#spr2 "./mediolania/melchior_2.png"
#name "King of Caelum"
#descr "When the Prophet Shrouded in White was born, it is said that a star guided three wise men, men of power and kings, to visit the Prophet and pay their respect, for the Prophet shall rule the world as the King of Kings, merciful and just beyond measure. He would bring eternal life and bounty and the world would be made perfect. Melchior is one of the three wise men. Melchior was an Eagle King in Caelum. One day six Celestial Yazatas appeared before him and implored him  to follow the star to meet the Prophet. Now his skeletal remains have stirred deep within the Holy Reliquary, as the Prophet gathers his armies and allies. His mortal remains are decorated with gold and sapphires, to emulate the icy equipment he once wore. The few feathers still preserved were put back on his wings. Melchior, as the Eagle Kings of Old, is a powerful Air mage, able to summon storms and lightning to smite the enemies of the King of kings. He is also knowledgeable to a lesser extent in the paths of Earth and Water, and gained some knowledge of Death after he died."
#fixedname "Melchior"
#weapon 75 --enchanted sword
#armor 75 -- fire plate
#armor 148 --crown
#hp 26
#size 4
#ressize 3
#mr 17
#str 15
#att 12
#def 13
#prec 12
#ap 9
#mapmove 22
#enc 0
#coldres 15
#poisonres 25
#shockres 10
#magicskill 1 4
#magicskill 2 1
#magicskill 3 1
#magicskill 5 1
#magicskill 9 3
#holy
#undead
#flying
#awe 4
#stormimmune
#mor 50
#mind
#undead
#magicbeing
#spiritsight
#neednoteat
--#noheal
#okleader
#okmagicleader
#goodundeadleader
#pierceres
#pooramphibian
#gcost 320
#humanoid
#unique
#latehero 15
#end

-- Gaspar of Ind
#newmonster 10072
#spr1 "./mediolania/gaspar.png"
#spr2 "./mediolania/gaspar_2.png"
#unmountedspr1 "./mediolania/gaspar_unm.png"
#unmountedspr2 "./mediolania/gaspar_unm.png"
#name "Magus of Ind"
#descr "When the Prophet Shrouded in White was born, it is said that a star guided three wise men, men of power and kings, to visit the Prophet and pay their respect, for the Prophet shall rule the world as the King of Kings, merciful and just beyond measure. He would bring eternal life and bounty and the world would be made perfect. Gaspar was one of the three wise men. Gaspar was one of the Magii that guided Ind before the rise of the Prester King. After a prophetic dream he followed a star to meet the prophet, riding on a camel across the Great Desserts. Now his skeletal remains have stirred deep within the Holy Reliquary, as the Prophet gathers his armies and allies. His mortal remains are decorated with gold, sapphires, emeralds and rubies and he is dressed in the style of the Ind of Old. Gaspar, as the Magii of Ind, is a powerful mage of the Stelar Sphere, well versed in the paths of Fire, Earth and the Stars. In life he also had insights into nature magic, and gained power over death after he died. Gaspar is able to divine the future and prevent bad events. His skeletal camel is intrinsically bound to him and will reform immediately after the battle should it fall."
#fixedname "Gaspar"
#unique
#armor 161 --"Jeweled Breastplate"
#armor 148 --crown
#weapon 745 --"Baculus"
#mountmnr 10022 -- skeletal camel
#regainmount 1
#hp 25
#size 3
#prot 0
#mr 20
#mor 50
#okleader
#okmagicleader
#okundeadleader
#str 12
#att 13
#def 13
#prec 13
#ap 24
#mapmove 26
#enc 0 
#coldres 15
#poisonres 25
#magicskill 0 2
#magicskill 3 1
#magicskill 4 3
#magicskill 5 1
#magicskill 6 1
#magicskill 9 3
#nobadevents 30
#wastesurvival
#holy
#undead
#neednoteat
--#heal
#pooramphibian
#pierceres
#gcost 320
#spiritsight
#humanoid
#latehero 15
#end

#newmonster 10022
#spr1 "./mediolania/skeletal_camel.png"
#spr2 "./mediolania/skeletal_camel_2.png"
#copystats 3829 -- sacred skeletal horse
#name "Skeletal Camel"
#descr "This skeletal camel is the faithful companion of Gaspar of Ind. Should it be destroyed in battle and Gaspar survives, it will immediately reform."
#cleararmor
#hp 12
#end

-- Balthasar of Machaka
#newmonster 10073
#spr1 "./mediolania/balthasar.png"
#spr2 "./mediolania/balthasar_2.png"
#name "King of Machaka"
#descr "When the Prophet Shrouded in White was born, it is said that a star guided three wise men, men of power and kings, to visit the Prophet and pay their respect, for the Prophet shall rule the world as the King of Kings, merciful and just beyond measure. He would bring eternal life and bounty and the world would be made perfect. Balthasar was one of the three wise men. Balthasar was one of the first Lion Kings and still remembered when the Lion Clan arrived to Great Mababwe. After consulting with the totemic spirits, it was revealed to him that he should follow a star and meet the person who shall one day tame even Lion. The next day a star appeared in the sky, and Balthasar went on his way. Now his skeletal remains have stirred deep within the Holy Reliquary, as the Prophet gathers his armies and allies. His mortal remains are decorated with gold, sapphires, emeralds and rubies. He wears a Kitharionic Lion Pelt, encrusted with jewels. His bones are painted black, to denote his machakan heritage. Balthasar is a powerful mage of fire, earth and nature, as he is a Lion King. He also gained power over death after he died."
#fixedname "Balthasar"
#unique
#armor 184 --Kitharionic lion pelt
#armor 148 --crown
#weapon 563 -- spirit club
#hp 30
#size 4
#prot 1
#invulnerable 18
#mr 16
#mor 50
#goodleader
#poormagicleader
#poorundeadleader
#str 16
#att 15
#def 15
#prec 10
#ap 13
#mapmove 22
#enc 0 
#coldres 15
#poisonres 25
#magicskill 0 2
#magicskill 3 2
#magicskill 5 1
#magicskill 6 3
#magicskill 9 3
#wastesurvival
#holy
#undead
#neednoteat
--#noheal
#pooramphibian
#pierceres
#gcost 320
#spiritsight
#humanoid
#latehero 15
#end


--Pope, prophet shape for bishops and archbishops
#newmonster 10074
#spr1 "./mediolania/pope.png"
#spr2 "./mediolania/pope_2.png"
#name "Pope"
#descr "The pope is the highest dignitary of the True God and the Prophet on the earthly plane, elected from the ranks of the most pious Archbishops, or rarely Bishops. He is the unquestioned leader of Mediolania and armies led by him will rarely waver. The True God grants Popes long lives and the gift to recuperate any wound or illness they may suffer."
#nametype 114 --Marignon man
#weapon 238 -- magic staff
#armor 158 --robes
#hp 15
#size 3
#mr 18
#mor 14
#str 10
#att 11
#def 11
#prec 11
#ap 10
#gcost 280
#holy
#heal
#startage 40
#maxage 500
#expertleader
#inspirational 2
#twiceborn 10060 --"Dignitary Saint"
#magicboost 9 1
#end

-- PRETENDERS

--Prophet shrouded in White
#newmonster 10075
#spr1 "./mediolania/proph_in_white.png"
#spr2 "./mediolania/proph_in_white_2.png"
#name "Holy Spirit"
#descr "When the Prophet Shrouded in White sacrificed themselves for the faithful, he ascended to the Heavenly Sphere. It is said that the prophet will return as the Holy Spirit, an ethereal apparition that will cleanse the world of the wicked and lead the believers to the Golden Afterlife. Now with the Pantokrator gone, the Holy Spirit manifests itself to guide the pious nation of Mediolania. Its holy splendour will awe those nearby and strike enemies of the True Faith with fear of the Judgment Day."
#fixedname "Jehoshua"
#weapon 238 -- magic staff
#weapon 597 -- intrsinsic great olm life drain
#gcost 250
#pathcost 60
#startdom 3
#hp 30
#size 3
#prot 10 --0
#mr 18 --20
#mor 30 --20
#goodleader
#expertundeadleader
#str 12
#att 12 --14
#def 12 --14
#prec 12 --13
#ap 20
#mapmove 22
#float
#stratage 600
#maxage 10000
#coldres 15
#poisonres 25
#fireres -10
#undead
#immortal
#ethereal
#heal
#awe 3
#fear 7
#neednoteat
#spiritsight
#magicskill 5 1
#magicskill 4 2
#speciallook 170 -- ethereal 
#humanoid
#end

-- Bone Archangel
#newmonster 10076
#spr1 "./mediolania/bone_archangel.png"
#spr2 "./mediolania/bone_archangel_2.png"
#name "Constructed Archangel"
#descr "To prove the glory of the Lord, the Archbishops of Mediolania constructed an angelic being using the bones of the most holy of martyrs. After countless prayers, led by the most pious of servants, the angel came to be inhabited by an Archangel of the Lord. Under the guidance of the Archangel, Mediolania is ready for the Ascension War and the pious shall receive the blessing of the Golden Afterlife. The Constructed Archangel is mindless and mostly does what its worshipers believe it would do. It punishes harshly and rewards sparingly."
#fixedname "Gabriel"
#weapon 95 --flambeu 
#armor 148 -- crown 
#gcost 260
#pathcost 80
#startdom 2
#hp 60
#size 8
#prot 0
#mr 18
#poorleader
#okundeadleader
#str 20
#att 13
#def 13
#prec 14
#ap 14
#mapmove 22
#enc 0
#mor 50
#startage 200
#maxage 1250
#flying
#undead
#inanimate
#neednoteat
#spiritsight
#pierceres
#coldres 15
#poisonres 25
#fireres 5
#shockres 5
#awe 5
#invulnerable 25
#magicbeing
#noheal
#magicskill 0 1 --F
#magicskill 5 1 --D
#unique
#end

-- Angel of Death
#newmonster 10077
#spr1 "./mediolania/angel_death.png"
#spr2 "./mediolania/angel_death_2.png"
#name "Angel of Death"
#descr "The Angel of Death is an angelic being tasked with dispensing merciful and just death. It judges the deceased, allowing the worthy to the Golden Afterlife in the celestial sphere, while the unworthy are given over to the Lords of the Underworld. With the disappearance of the Pantokrator, the Angel of Death will don the mantle of godhood to bring salvation to the worthy, and punishment to the wicked. It wields a scythe that banishes the wicked to the inferno."
#fixedname "Samael"
#weapon 310 -- infernal scythe
#gcost 280
#pathcost 80
#startdom 3
#hp 50
#size 6
#prot 0
#mr 18
#mor 30
#superiorleader
#okmagicleader
#superiorundeadleader
#str 14
#att 14
#def 14
#prec 15
#ap 16
#mapmove 28
#enc 1
#startage 600
#maxage 2500
#magicskill 1 1 --A1
#magicskill 5 2 --D2
#flying
#neednoteat
#spiritsight
#fireres 5
#shockres 5
#awe 5
#fear 5
#invulnerable 25
#magicbeing
#end

-- =========== SPELLS ======================

-- RITUAL

-- Enchantment

-- Summon Battle Relic Commander
#newspell
#name "Consecrate Battle Relic"
#descr "A holy relic is taken from the Holy Reliquary, consecrated, and placed in a fine golden cask. It will be carried into battle where it will inspire the faithful. Pilgrims will come to see the relic and follow it in battle."
#restricted 199 --"Mediolania"
#effect 10021 --summon commander
#damage 10058 --"Battle Relic"
#nreff 1
#onlyatsite "Holy Reliquary"
#school 4 --enchantment
#researchlevel 3
-- #researchlevel 0
#path 0 5
#path 1 9
#pathlevel 0 2
#pathlevel 1 2
#fatiguecost 1500 --15 D gems
#end


-- 1x Summon Catacomb Martyrs 
#newspell
#name "Baptize Catacomb Martyr"
#descr "A high church dignitary re-baptizes and oversees the equipment of a holy Catacomb Martyr. Bodies of ancient unnamed Martyrs are equipped with gilded arms and armor and adorned with jewels to do battle upon the enemies of the Church and the Prophet Shrouded in White. They are sacred to the people of Mediolanum and their beautifully adorned equipment is said to awe their enemies. They are constantly surrounded by faithful and pilgrims which repair any battle damage. This however means that Catacomb Saints cost upkeep."
#restricted 199 --"Mediolania"
#onlyatsite "Holy Reliquary"
#school 4 --enchantment
#researchlevel 2
-- #researchlevel 0
#path 0 5
#path 1 9
#pathlevel 0 1
#pathlevel 1 2
#effect 10001 --summon unit
#fatiguecost 200 --2D gems
#damage 10010 --"Catacomb Martyr"
#nreff 1
#end

-- 8 + 1/2 Summon Catacomb Martyrs 
#newspell
#name "Baptize Catacomb Centuria"
#descr "A high church dignitary re-baptizes and oversees the equipment of a centuria of holy Catacomb Martyrs.Bodies of ancient unnamed Martyrs are equipped with gilded arms and armor and adorned with jewels to do battle upon the enemies of the Church and the Prophet Shrouded in White. They are sacred to the people of Mediolanum and their beautifully adorned equipment is said to awe their enemies. They are constantly surrounded by faithful and pilgrims which repair any battle damage. This however means that Catacomb Saints cost upkeep."
#restricted 199 --"Mediolania"
#onlyatsite "Holy Reliquary"
#school 4 --enchantment
#researchlevel 4
-- #researchlevel 0
#path 0 5
#path 1 9
#pathlevel 0 2
#pathlevel 1 2
#effect 10001 --summon unit
#fatiguecost 1400 --14D gems
#damage 10010 --"Catacomb Martyr"
#nreff 508 -- 8 + 1/2
#end

-- 24 Summon Catacomb Martyrs 
#newspell
#name "Baptize Catacomb Cohort"
#descr "A high church dignitary re-baptizes and oversees the equipment of an entire cohort of holy Catacomb Martyrs.Bodies of ancient unnamed Martyrs are equipped with gilded arms and armor and adorned with jewels to do battle upon the enemies of the Church and the Prophet Shrouded in White. They are sacred to the people of Mediolanum and their beautifully adorned equipment is said to awe their enemies. They are constantly surrounded by faithful and pilgrims which repair any battle damage. This however means that Catacomb Saints cost upkeep."
#restricted 199 --"Mediolania"
#onlyatsite "Holy Reliquary"
#school 4 --enchantment
#researchlevel 6
-- #researchlevel 0
#path 0 5
#path 1 9
#pathlevel 0 4
#pathlevel 1 3
#effect 10001 --summon unit
#fatiguecost 3200 --32D gems
#damage 10010 --"Catacomb Martyr"
#nreff 24
#end

-- Summon Catacomb Saint Commander 
#newspell
#name "Canonize Catacomb Saint"
#descr "Named saints in Mediolania are kept in particularly high regard. With this spell a high ranking church official canonizes the bones of a Saint and pleads for their help. With prayers and belief, the bones of a longdead Saint animate to serve Mediolania and the Awakening God! They mostly follow what the people believe they would do. Catacomb saints are divided into Soldier Saints, Dignitary Saints, and Hierophant Saints. Their jewelled armor awes their enemies while any mortal in their presence is forced to reckon their own mortality. They are constantly surrounded by faithful and pilgrims which repair any battle damage. This however means that Catacomb Saints cost upkeep."
#restricted 199 --"Mediolania"
#effect 10021 --summon commander
#damage -6660 --random "Catacomb Saint"
#nreff 1
#onlyatsite "Holy Reliquary"
#school 4 --enchantment
#researchlevel 5
-- #researchlevel 0
#path 0 5
#path 1 9
#pathlevel 0 3
#pathlevel 1 3
#fatiguecost 3000 --3500
#end


-- Construction

#newspell
#name "Enchant Memento Mori"
#descr "Several skulls are taken and wings constructed using raven feathers. Then, they are enchanted with death magic to whisper in the ears of the population about their eventual death and demise. These Memento Mori, decrease unrest wherever they are. In times of war they can be used to paralyze enemies with whispers and visions of death."
#restricted 199 -- "Mediolania"
#school 3 -- Const
#researchlevel 2
-- #researchlevel 0
#path 0 5
#pathlevel 0 2
#effect 10001 --summon unit
#fatiguecost 300 --3D gems
#damage 10012 --"Memento Mori"
#nreff 1003
#end

#newspell
#name "Build Charnel"
#descr "A high priest commissions the local populace and monks to excavate, clean and arrange the skulls of the commoners of Mediolania to erect a Charnel. The Charnel is then blessed and used as a conduit to the Prophet Shrouded in White and the True God. The populace will gather there and contemplate mortality. The Charnel spreads dominion order and reduces unrest. In battle it will smite heretics."
#restricted 199 --"Mediolania"
#effect 10021 --summon commander
#damage 10066 -- "Charnel"
#nreff 1
#school 3 --const
#researchlevel 3
#path 0 5
#path 1 9
#pathlevel 0 1
#pathlevel 1 2
#fatiguecost 1200 --12 D gems
#end

#newspell
#name "Channel Angel of the Choir"
#descr "A Priest of the Prophet takes the body of a Martyr and constructs wings of bone. With enchantments and communal prayers, a minor Angel of the True God is summoned into the bony body. The people of Mediolania believe it to be a member of the heavenly Choir, so it sings the heavenly music and joins communions on the battlefield automatically."
#restricted 199 --"Mediolania"
#effect 10001 --summon monster
#damage 10013 --"Angel of the Choir"
#nreff 1
#onlyatsite "Holy Reliquary"
#school 3 --enchantment
#researchlevel 4
-- #researchlevel 0
#path 0 4
#path 1 9
#pathlevel 0 2
#pathlevel 1 2
#fatiguecost 500 -5 S gems
#end

#newspell
#name "Channel Angel of Judgment"
#descr "A Priest of the Prophet takes the body of a saint and constructs wings of bone. With enchantments and communal prayers, an Angel of the True God is summoned into the bony body. As it follows the will and beliefs of the people it has angelic attributes such as invulnerability to mundane weapons, awe and magic of the heavens. Its trumpet will call the dead to be judged and the faithful dead will raise to protect Mediolania, while the unfaithful will be turned to ash by the power of the trumpet."
#restricted 199 --"Mediolania"
#effect 10021 --summon commander
#damage 10068 --"Angel of Judgment"
#nreff 1
#onlyatsite "Holy Reliquary"
#school 3 --enchantment
#researchlevel 6
-- #researchlevel 0
#path 0 4
#path 1 9
#pathlevel 0 3
#pathlevel 1 2
#fatiguecost 2500 -25 S gems
#end



#newspell
#name "Bone Angel Construction"
#descr "A Priest takes the body of a saint and constructs wings from the bones of revered bishops and archbishops. Raven feathers are then used to complete the wings. With enchantments and communal prayers lasting a month a Bone Angel arises. As it follows the will and beliefs of the people it has angelic attributes such as invulnerability to mundane weapons, awe and magic of the heavens. Any mortal in their presence is forced to reckon their own mortality."
#restricted 199 --"Mediolania"
#effect 10021 --summon commander
#damage 10065 --"Bone Angel"
#nreff 1
#onlyatsite "Holy Reliquary"
#school 3 --construction
#researchlevel 7
#path 0 5
#path 1 9
#pathlevel 0 4
#pathlevel 1 2
#fatiguecost 4500 -45 D gems
#end


--Conjuration

-- Summon Capuchin 
#newspell
#name "Commission Capuchin Friar"
#descr "With a small offering of magic Pearls, a Capuchin Brother is commissioned to serve Mediolania. This secretive sect has perfected the art of making Mummies and each brother can create 5 per month. To be noted however, a small monthly stipend needs to be donated to the Capuchins for every Mummy."
#restricted 199 --"Mediolania"
#effect 10021 --summon commander
#damage 10062 --"Capuchin Brother"
#nreff 1
#school 0 --conjuration
#researchlevel 4
#path 0 4
#path 1 9
#pathlevel 0 2
#pathlevel 1 2
#fatiguecost 2100 --15
#end

-- Summon Mother Supperior
#newspell
#name "Shepherd of Virgins"
#descr "Using some astral pearls and godly authority, a priest mage of the true fate calls to one of the wandering Mother Superiors, who scour the countryside for virgins to join their convents. The long years spent finding innocent women left them particularly attuned to those of pure blood. Unfortunately, as a side effect, they gained insight into blood magic, something they are strictly forbidden to practice, yet may reluctantly resort to when their life is endangered on the field of battle."
#restricted 199 -- "Mediolania"
#effect 10021 --summon commander
#damage 10063 --"Mother Superior"
#nreff 1
#school 0 --conjuration
#researchlevel 5
-- #researchlevel 0
#path 0 4
#path 1 9
#pathlevel 0 2
#pathlevel 1 3
#fatiguecost 2200 -21
#end

-- Summon Sepolta viva

#newspell
#name "Plead with the Sepolte Vive"
#descr "The Nun order of the Sepolte Vive - meaning buried alive, takes corporal mortification and morbidity to the extreme. They sleep in coffins, inside ossuaries decorated with the bones of former nuns. If one of them dies they are not buried, instead they are left where they died so that others might contemplate mortality and see the decay of the earthly body. Therefore, they are extremely attuned to death magic. Acquiring the service of one is not easy, as they never leave their ossuaries. It will require incredible religious authority and the donation of 33 new virgin members to the order." 
#restricted 199 -- "Mediolania"
#effect 10021 --summon commander
#damage 10064 --"Sepolta Viva"
#nreff 1
#school 0
#researchlevel 6
-- #researchlevel 3
-- #researchlevel 0
#path 0 8
#path 1 9
#pathlevel 0 1
#pathlevel 1 3
#fatiguecost 3300
#end

-- Replace skeleton summoning spells

#newspell
#copyspell 1113 -- Reanimation
#name "Reanimate Legionaires"
#descr "The necromancer enchants ten well-prepared corpses and gives them false life. Skeletons are undead and will fall apart if left on the battlefield without undead leadership."
#restricted 199 -- mediolania
#damage -6661
#end

#newspell
#copyspell 1111 -- Animate Skeleton
#name "Animate Legionaire"
#descr "The necromancer enchants the bones of a fallen warrior, giving it false life. Skeletons will fall apart if left on the battlefield without a commander."
#restricted 199 -- mediolania
#damage -6661
#end

#newspell
#copyspell 1142 -- Raise Skeletons
#name "Raise Legionaires"
#descr "The necromancer enchants the bones of a handful warriors, giving them false life. Skeletons will fall apart if left on the battlefield without undead leadership."
#restricted 199 -- mediolania
#damage -6661
#end

#newspell
#copyspell 1184 -- Horde of Skeletons
#name "Host of Legionaires"
#descr "The necromancer enchants the bones of the dead and calls forth a horde of Longdead Warriors."
#restricted 199 -- mediolania
#damage -6661
#end

#selectspell 1113 -- Reanimation
#notfornation 199 - Mediolania
#end

#selectspell 1111 -- Animate Skeleton
#notfornation 199 - Mediolania
#end

#selectspell 1142 -- Raise Skeletons
#notfornation 199 - Mediolania
#end

#selectspell 1184 -- Horde of Skeletons
#notfornation 199 - Mediolania
#end


#newspell
#name "Days of Judgement"
#descr "With this powerful enchantment, the End Times are proclaimed and the unfaithful shall be judged! Undead will rise in friendly dominion to serve the True God in hopes of redemption. Preachers of false faiths inside strong dominion may get attacked by angels bringing God's wrath upon the infidel."
#details "Every friendly province has a 10*Dominion Strength % chance to spawn 1d6 Longdeads, including ermorian ones if dominion 5 or lower. Dom 6 and 7 provinces spawn 1d6 Longdead. Dom 8 and 9 provinces 2d6 and dom 10+ 3d6 longdead. Enemy Priests in provinces with friendly dominion have a 2*(Dominion Strength)% chance to get an assasinnation attempt by an Angel of Fury."
#restricted 199 -- mediolania
#school 4
#researchlevel 8
#path 0 4
#path 1 5
#pathlevel 0 4
#pathlevel 1 4
#effect 10081
#damage 660 -- Days of Judgment
#nreff 1
#fatiguecost 7500 -- 75 S gems
#end


--COMBAT 


--Unholly Command
#newspell
#name "Undead Repentance"
#descr "A Priest of Mediolania forces an enemy undead to repent and serve the Prophet as atonement."
#restricted 199 --"Mediolania"
#school 7
#path 0 9
#pathlevel 0 2
#effect 28
#damage 999
#range 20
#nreff 1
#aoe 0
#spec 293863560
#end


--Unholly Blessing lvl 2 analog
#newspell
#name "Blessed be the Martyrs"
#descr "With this spell a Bishop of Mediolania confers the blessing of the Prophet to a large number of sacred undead. These undead Martyrs will be given boons from the Prophet himself!"
#restricted 199 --"Mediolania"
#school 7
#path 0 9
#pathlevel 0 2 --H2
#effect 10
#damage 1
#range 20
#aoe 15
#nreff 1
#precision 100
#spec 281067528
#end


-- Protection of the Sepulcher analog
#newspell
--#copyspell 291 -- protection of the sepulcher
#name "Protection of the Prophet"
#descr "With this prayer a powerful priest grants increased magic resistance to all sacred martyrs on the battlefield. The blessed dead will be harder to banish by heretical priests."
#restricted 199 --"Mediolania"
#school 7
#path 0 9
#pathlevel 0 4 -- Holy 4
--#fatiguecost 50 -- ??
#aoe 666
#effect 10 -- effect category 10
#damage 67108864 -- MR + 4
#nreff 1
#precision 100
#spec 281051144 --affect demons and undead, friendlies only, may use underwater, no effect on demons, sacred only
#end
 
-- Power of the Sepulcher analog
#newspell
--#copyspell 292 -- power of the sepulcher 
#name "Power of the Prophet"
#descr "With this prayer a powerful priest grants increased movement speed and attack skill to all sacred undead on the battlefield."
#restricted 199 --"Mediolania"
#school 7
#path 0 9
#pathlevel 0 5 -- Holy 5
--#fatiguecost 50 -- ??
#aoe 666
#effect 23 -- effect category 23
#damage 33554432 -- Unholy power
#nreff 1
#precision 100
#spec 281051144 --affect demons and undead, friendlies only, may use underwater, no effect on demons, sacred only
#end

-- H2 communion slave
#newspell
#copyspell 1264
#name "Holy Choir"
#descr "With this prayer a high priest or Bishop enters into communal prayer and becomes a communion slave."
#restricted 199 --"Mediolania"
#school 7
#path 0 9
#pathlevel 0 2
#researchlevel 0
#fatiguecost 10
#end

-- H2 communion master
#newspell
#copyspell 1263
#name "Choir Leader"
#descr "With this prayer a high priest or Bishop enters into communal prayer and becomes a communion master."
#restricted 199 --"Mediolania"
#school 7
#path 0 9
#pathlevel 0 2
#researchlevel 0
#fatiguecost 10
#end


--H7 Anti-undead
#newspell
#copyspell 448 --holy pyre
#name "Holy Chastisement"
#descr "The only true path to the Afterlife is through the power of the True God and the Prophet Shrouded in White! With this powerful spell a holy choir invokes the God's power over the afterlife. Enemy undead will be burned to cinders by the holy wrath of God. Powerful undead may resist both effects."
#restricted 199 --"Mediolania"
#school 7
#path 0 9
#pathlevel 0 7
#researchlevel 0
#aoe 666
#spec 293879912--demons and undead, heat/fire, armor piercing, ignores shields, only enemies, mr easy, may use UW, no demons
#end  

--========= ITEMS =========

#selectitem "Shroud of the Battle Saint"
#nationrebate 199 --"Mediolania"
#end

#selectitem "Flask of Holy Water"
#nationrebate 199 --"Mediolania"
#end

#newitem
#spr "./mediolania/arm_proph.png"
#name "Armatura Prophetae"
#descr "This blessed armor includes a sacred replica of the Shroud and marks the wearer as a warrior of the Prophet Shrouded in White. This grants the wearer sacred status as well as recuperation abilities. However only beings that have faced mortality may use it, and therefore it is relegated to the undead."
#restricted 199 --"Mediolania"
#type 5
#armor 110 --"Armor of Virtue"
#constlevel 6
#mainpath 4
#secondarypath 5
#mainlevel 2
#secondarylevel 2
#heal
#bless
#onlyundead
#nofind
#hp 6
#end

#selectitem 740
#clear
#spr "./mediolania/trumpet_judgment.png"
#name "Heavenly Horn"
#descr "This Holy Trumpet will call the dead to judgement. The faithful will rise to protect Mediolania and the Prophet Shrouded in White, while the heretic undead shall be destroyed by its sound."
#restricted 199 --"Mediolania"
#type 3 -- missile weapon
#weapon 145 --heavenly horn
#constlevel 6
#mainpath 1
#secondarypath 5
#mainlevel 2
#secondarylevel 1
--#autospell "Raise Skeletons"
#autospell "Animate Legionaire"--"Animate Skeleton"
#autospellrepeat 1
#end

-- Saint's Blood (bless, disease resistance, poison resistance)
#newitem
#spr "./mediolania/saint_blood.png"
#name "Vial of Martyr's Blood"
#descr "In Mediolania preserved body parts of ancient martyrs are commonplace. These relics bless the bearer if sacred to the true god. This holy vial contains the blood remains of a sanctified martyr. The blood is miraculously still liquid, despite the martyr being dead for a thousand years. The blood of the sacred martyr helps prevent disease and ill-effects of poison."
#restricted 199 --"Mediolania"
#type 8
#poisonres 10
#diseaseres 75
#autobless
#constlevel 2
#mainpath 4
#mainlevel 1
#end

-- Saint's Foot (mapmove, quickness?, reinvigoration)
#newitem
#copyitem 302 -- boots of the spider
#spr "./mediolania/saint_foot_small.png"
#name "Martyr's Foot"
#descr "In Mediolania preserved body parts of ancient martyrs are commonplace. These relics bless the bearer if sacred to the true god. This is the preserved foot of a holy Martyr. Many such martyrs were wayfarers and itinerant healers or preachers. It is believed that the feet of such martyrs help with travel. The bearer of such a relic will feel reinvigorated and able to move faster and longer distances before tiring. He will be unhindered by terrain and entanglement spells will be easier to resist."
#restricted 199 --"Mediolania"
#armor 0
#type 8
#mapspeed 12
#swift 100
#autobless
#constlevel 4
#mainpath 2
#secondarypath 5
#mainlevel 1
#secondarylevel 1
--#itemdrawsize -50
#end

-- Saint's Head (spirit sight, angel of the host retinue?, holy words?, autospell?)
#newitem
#spr "./mediolania/saint_head.png"
#name "Martyr's Head"
#descr "In Mediolania preserved body parts of ancient martyrs are commonplace. These relics bless the bearer if sacred to the true god. The head of a Martyr is a very prized possession. The head is animated by prayer and death magic, uttering words most holy. This is particularly effective against holy warriors of False Gods who are stunned by the words of a True God's martyr. It will also utter words of eternal damnation awaiting those who don't follow the true god, extruding an aura of fear."
#restricted 199 --"Mediolania"
#haltheretic 10
#autospell "Holy Word"
#autospellrepeat 1
#autobless
#fear 5
#constlevel 6
#mainpath 5
#mainlevel 2
#end

-- Saint's Heart (recuperation, damage reversal?? too powerful??)
#newitem
#spr "./mediolania/saint_heart.png"
#name "Heart of a Martyr"
#descr "In Mediolania preserved body parts of ancient martyrs are commonplace. These relics bless the bearer if sacred to the true god. The heart of a martyr is the most prized possession, as all the purity and goodliness resides there. Few mortals would dare strike someone carrying this most holy of relics. In the event the bearer would be stuck down, the martyr performs one last act of martyrdom and sacrifices the heart instead, crumbling to dust but granting the user another chance at life."
#restricted 199 --"Mediolania"
#autobless
#extralife 1
#awe 3
#constlevel 6
#mainpath 4
#secondarypath 5
#mainlevel 3
#secondarylevel 2
#end

-- A unique extra powerful const8 holy shroud ??
#newitem
#spr "./mediolania/holy_shroud.png"
#name "Holy Shroud"
#descr "The restored Holy Shroud of the Prophet. With magic and prayer the most holy of relics has been restored from merely a few fragments that remained. It extrudes an aura of magnificence. Those worthy enough to wear this holiest of relics will be reinvigorated and regenerated by the ever-fresh blood staining the shroud. Few would dare strike something so holy, and if they do they will find that wounds appear on their own person instead of the wearer. Mundane weapons will prove to be completely ineffective. Those wearing the shroud will be blessed, regardless of the sacred status. There is but one holy shroud and should it somehow be destroyed in battle, it must once more be restored to its glory."
#restricted 199 --"Mediolania"
#armor 54
#bless
#awe 5
#damagerev 2
#invulnerable 25
#regeneration 10
#reinvigoration
#cursed
#nofind
#unique
#hp 10
#constlevel 8
#mainpath 4
#secondarypath 5
#mainlevel 3
#secondarylevel 3
#end 


--======== NAME POOL ========== 

-- General Saints
#selectnametype 288
#clear
#addname "St. Achileus"
#addname "St. Albertus"
#addname "St. Andreas"
#addname "St. Auxelius"
#addname "St. Benedictus"
#addname "St. Benerose"
#addname "St. Birgitta"
#addname "St. Bonifatius"
#addname "St. Canditus"
#addname "St. Deodatus" -- generic name
#addname "St. Dominicus"
#addname "St. Domitilla"
#addname "St. Felix"
#addname "St. Fides"
#addname "St. Gallus"
#addname "St. Getreu"
#addname "St. Hyacinthus" -- generic name
#addname "St. Irenaus"
#addname "St. Jakobus"
#addname "St. Johann"
#addname "St. Julianus"
#addname "St. Kilian"
#addname "St. Konstatinus"
#addname "St. Laurentia"
#addname "St. Laurentius"
#addname "St. Leo"
#addname "St. Leontius"
#addname "St. Luciana" --pg 60.
#addname "St. Maergen"
#addname "St. Martin"
#addname "St. Martina"
#addname "St. Markus"
#addname "St. Maximus"
#addname "St. Munditia"
#addname "St. Nereus"
#addname "St. Nikolaus"
#addname "St. Pancratius" -- :)
#addname "St. Placidus"
#addname "St. Severina"
#addname "St. Silvester"
#addname "St. Symphorosa"
#addname "St. Theodosius"
#addname "St. Valentin"
#addname "St. Valerius"
#addname "St. Venantius"
#addname "St. Verena"
#end

-- Fourteen Holy Helpers
#selectnametype 289
#clear
#addname "St. Agathius"
#addname "St. Barbara"
#addname "St. Blaise"
#addname "St. Catherine"
#addname "St. Christopher"
#addname "St. Cyriacus"
#addname "St. Denis"
#addname "St. Erasumus"
#addname "St. Eustace"
#addname "St. George"
#addname "St. Giles"
#addname "St. Margaret"
#addname "St. Pantaleon"
#addname "St. Vitus"
#end

--============= EVENTS ==================


-- Charnel Trouble 
#newevent 
#rarity 1 --common bad
#req_fornation 199
#req_nation 199
#req_targmnr 10066 --"Charnel"
#req_nomonster 10056 --"Archbishop of the Second Coming"
#msg "The Population of this province has committed Idolatry, and worships the skulls in the Charnel instead of the True God. Faith will decrease as long as the Charnel is not purified. The offerings the people leave, however, can be collected by the church to finance Mediolania. An Archbishop should be sent to bring the flock back to the righteous path and cleanse the Charnel."
#transform 10067 --"Idolatrous Charnel"
#end

#newevent
#rarity 0 --always but once per province, one charnel purified per turn
#req_fornation 199
#req_nation 199
#req_targmnr 10067 -- "Idolatrous Charnel"
#req_monster 10056 --"Archbishop of the Second Coming"
#msg "The Archbishop purified the Charnel and reprimanded the populace! Faith increased and chants are sung to the True God !" 
#transform 10066 --"Charnel"
#incdom 1
#end

-- Finding Saints

#newevent
#rarity -2 -uncommon good
#req_land 1
#req_fornation 199
#req_nation 199
#req_fullowner 199 -- Dominion + province ownership
#req_foundsite 1
#msg "The skeleton of an ancient Martyr has been found in the Ruins of the Old Empire! The bones have been cleaned and sealed. They should be brought to the Holy Reliquary in the capital to be cleansed, rebaptised, blessed and equipped so the saint may join the armies of the Prophet! [Ruins of the Old Empire]"
#nation 199
#com 10069 --"Found Saint"
#end

#newevent
#rarity -2 -uncommon good
#req_land 1
#req_fornation 199
#req_nation 199
#req_fullowner 199 -- Dominion + province ownership
#req_foundsite 1
#msg "The skeleton of an ancient Martyr has been found in the Catacombs! The bones have been cleaned and sealed. They should be brought to the Holy Reliquary in the capital to be cleansed, rebaptised, blessed and equipped so the saint may join the armies of the Prophet! [Catacombs]"
#nation -2 --province owner
#com 10069 -- "Found Saint"
#end

#newevent
#rarity 5 --always unlimited 
#req_fornation 199
#req_nation 199
#req_fullowner 199 -- Dominion + province ownership
#req_foundsite 1
#msg "The skeleton of an ancient Martyr has been brought to the capital! It has been cleansed, blessed and armed to fight for the Prophet! [Holy Reliquary]"
#req_targmnr 10069 --"Found Saint"
#transform -6660 --"Catacomb Saint"
#end


-- GLOBAL
#newevent
#rarity 13
#req_myench 660
#req_owncapital 1
#req_unique 1
#req_pop0ok
#msg "A dire portent.
Mediolania has declared the coming of the Days of Judgment and the ascension of ##godname##. The dead stir inside ##godname##'s dominion seeking redemption by joining the armies of Mediolania. Meanwhile priests of foreign faiths inside ##godname##'s dominion may get attacked by heavenly angels of fury. The Days of Judgment surely mean that the ascension of the God of Mediolania is at hand!"
#nation 0
#end

#newevent
#rarity 0
#nation -2
#req_fornation 199
#req_domowner 199
#req_friendlyench 660
#req_pop0ok
#req_fullowner 199 -- mediolanian dominion and province owned by mediolania
#req_maxdominion 5 --dom 5
#msg "Dom1-5 spawn"
#notext
#nolog
#1d6units -6661
#end

#newevent
#rarity 0
#nation -2
#req_fornation 199
#req_domowner 199
#req_friendlyench 660
#req_fullowner 199 -- mediolanian dominion and province owned by mediolania
#req_dominion 6
#req_maxdominion 7 
#req_pop0ok 
#msg "Dom6-7 spawn"
#notext
#nolog
#1d6units -6661
#end

#newevent
#rarity 0
#nation -2
#req_fornation 199
#req_domowner 199
#req_friendlyench 660
#req_fullowner 199 -- mediolanian dominion and province owned by mediolania
#req_dominion 8
#req_maxdominion 9 
#req_pop0ok 
#msg "Dom8-9 spawn"
#notext
#nolog
#2d6units -6661
#end

#newevent
#rarity 0
#nation -2
#req_fornation 199
#req_domowner 199
#req_friendlyench 660
#req_fullowner 199 -- mediolanian dominion and province owned by mediolania
#req_dominion 10
#req_pop0ok
#msg "Dom10+ spawn"
#notext
#nolog
#3d6units -6661
#end

#newevent
#rarity 5
#req_domchance 2
#nation 199 -- event owned by mediolania
#req_notfornation 199
#req_hostileench 660
#req_domowner 199
#req_pop0ok
#req_targpath1 9 -- priest 1 or higher
#assassin 1369 -- Angel of Fury
#assowner 199 --mediolania
#msg "Suddenly an Angel of Fury descended from the heavens and tried to assassinate your priest!"
#nolog
#end

-- =========== SITES =================

#newsite 1790
#name "Cathedral of the Second Coming"
#path 9 --icon
#level 0
#rarity 5
#gems 0 1
#gems 4 1
#homemon 10008 --"Equite of the Second Coming"
#homecom 10057 --"Mediolanum Architect"
#homecom 10056 --"Archbishop of the Second Coming"
#loc 16384
#end

#newsite 1791
#name "Holy Reliquary"
#path 9 --icon
#level 0
#rarity 5
#gems 5 2
#loc 16384
#summonlvl2 10010 --catacomb martyrs
#end

#newsite 1792
#name "Mediolania Summons"
#path 4 --icon
#level 0
#rarity 5
#homecom 10058
#homecom 10059
#homecom 10060
#homecom 10061
#homecom 10062
#homecom 10063
#homecom 10064
#homecom 10065
#homecom 10066
#homecom 10068
#homemon 10010
#homemon 10011
#homemon 10012
#homemon 10013
#end

#newsite 1793
#name "Mediolania Heroes"
#path 8 --icon
#level 0
#rarity 5
#homecom 10070
#homecom 10071
#homecom 10072
#homecom 10073
#homecom 10074
#end

--=========== NATION =================

#selectnation 199
#clear
#name "Mediolania"
#epithet "The Second Coming"
#era 3
#aideathnation
#brief "Mediolania worships the skeletons of Ermor as Martyrs and awaits the second coming of the Prophet Shrouded in White"
#descr "Mediolania is an ancient Ermorian province on the border of Eldergate. During the crusades against the undead legions of Ermor, Marignon settled and fortified Mediolania as a border province and staging ground. Many zealots and preachers flocked to the city in those times, and soon a new religion started to emerge. The undead legions were a punishment and test for the true believers, who awaited the second coming of the Prophet Shrouded in White. Through suffering, penitence and contemplation of death, which was literally on their doorstep, the true believers will be granted eternal life. Although heavily persecuted by the Inquisition, the cult flourished when catacombs filled with dead Ermorian martyrs were found underneath the city. Seeing this as proof of divine guidance, the bishops of the new religion seized power. Mediolania now worships the skeletons still found in the catacombs, and Eldergate itself, as martyrs. The dead are dressed in fineries, decorated with jewels and armored in gilded plate. Martyrs are reanimated by collective prayer and their will and advice heeded in every way as the will of the Prophet Shrouded in White itself. The skeletons of the faithful are used in ceremonies contemplating mortality and rights of resurrection. They must serve the church even after death until the Day of Judgment, when the Prophet Shrouded in White returns and the Awakening God ascends. Only then will the faithful be granted a place in the Golden Afterlife. Pilgrims loot old Ermorian equipment they deem blessed and frequently join the armies of Mediolania. The backbone of the army, however, remains the classical Marignon infantry. The people of Mediolania have embraced death, and a death dominion will not affect them as much, however neither will growth dominion."
#summary "Race: Humans. Death and Growth Scales have half the standard effect on income and population growth  
Military: Marignon style regulars bolstered by religious fanatics and sacred undead 
Magic: Death, astral, fire, earth, some water.
Priests: Strong." 
#flag "./mediolania/flag.png"
#templepic 9
#color 0.65 0.38 0.75
#homefort 4
#halfdeathinc
#halfdeathpop

#moregrowth -1
#moreorder 1

-- START SITES

#fortera 3
#startsite "Cathedral of the Second Coming"
#startsite "Holy Reliquary"
#futuresite 1792
#futuresite 1793


-- PRETENDERS

#homerealm 3 --mediterranean
#addgod 179 --"Master Lich"
#addgod 180 --"Demilich"
#addgod 215 --"Virtue"
--#addgod 395 --"Lich Queen"
#addgod 872 --"Ghost King"
#addgod 874 --"Divine Emperor"
#addgod 1025 --"Divine Glyph"
-- #addgod "Neter of the Underworld"
#addgod 2789  --"Raven of the Underworld"
#addgod 158 -- oracle
#addgod 249 -- Crone
#addgod 251 --great sage
#addgod 10075 
#cheapgod20 10075 
#addgod 10076
#addgod 10077

-- HEROES

#multihero1 10069 --14 holy helpers
#hero1 10070 -- Melchior of Caelum
#hero2 10071 -- Gaspar of Ind
#hero3 10072 -- Balthasar of Machaka

-- ADD SOLDIERS

#addrecunit 10000 --"Crossbow Militia"
#addrecunit 10001 --"Pavise Crossbowman"
#addrecunit 10002 --"Mediolanum Pikeneer"
#addrecunit 10003 --"Mediolanum Halberdier"
#addrecunit 10004 --"Ulmish Greatsword"
#addrecunit 10007 --"Mediolanum Pilgrim"


-- ADD COMMANDERS

#addreccom 426 --Generic Scout
#addreccom 10050-- "Mediolanum Centurion"
#addreccom 10051 --"Member of the Ducal Family"
#addreccom 10052 --"Mediolanum Monk"
#addreccom 10053 --"Caretaker Nun"
#addreccom 10054 -- "Master Crafter"
#addreccom 10055 -- "Mediolanum Bishop"

-- PD

#defcom1 10050 --"Mediolanum Centurion"
#defcom2 10051 --"Member of the Ducal Family"
#defunit1 10002 -- "Mediolanum Pikeneer" 
#defunit1b 10000 -- "Crossbow Militia"
#defunit2 10003 -- "Mediolanum Halberdier"
#defunit2b 10001 -- pavise crossbow

#wallcom 10050 --centurion
#wallunit 10000 --"Crossbow Militia"
#wallmult 10

#guardcom 10051 --"Member of the Ducal Family"
#guardunit 10009 -- foot knight 
#guardmult 10

--Sets how many of the units to appear per point.

#defmult1 10
#defmult1b 10
#defmult2 10
#defmult2b 10

#startcom 10050 --"Mediolanum Centurion" 
#startunittype1 10002 --"Mediolanum Pikeneer" 
#startunitnbrs1 20
#startunittype2 10001 --"Pavise Crossbowman" 
#startunitnbrs2 10
#startscout 426 -- Generic Scout

#end

