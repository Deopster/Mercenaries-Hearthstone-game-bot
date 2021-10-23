# Hearthstone-Mercenaries-game-bot
```diff
- prevention: Bot is not ready and now on the development stage
- estimated release date - works as fast as possible シ
```
<h3 align="center">Dev progress</h3>
<table>
  <tr>
    <td width=500vw>2560x1440</td>
     <td width=500vw>1920x1080</td>
  </tr>
  <tr>
    <td>
<ol>
<li>auto assembly of the group - ✓ </li>
<li>Checking and regrouping if the heroes have reached level 30 - ✓</li>
<li>Transition to level selection - ✓</li>
<li>transition between sublevels - ✓, ✗ (stranger don't work)</li>
<li>Choosing a reward after passing a level - ✓</li> 
<li>Putting heroes on the board - ✓</li>
<li>searching for suitable opponents - ✓</li>
<li>choosing abilities - ✓</li>
<li>attacking opponents - ✓</li>
<li>collecting rewards for reaching the last level-  ✗</li>
<li>repeat from 1 point - ✗</li>
</ol>
      <br><br>
    </td>
    <td><ol>
<li>auto assembly of the group - ✓ </li>
<li>Checking and regrouping if the heroes have reached level 30 - ✓</li>
<li>Transition to level selection - ✓</li>
<li>transition between sublevels - ✓ </li>
<li>Choosing a reward after passing a level - ✓</li> 
<li>Putting heroes on the board - ✓</li>
<li>searching for suitable opponents - ✓,✗(not finding green and blue)</li>
<li>choosing abilities - ✓</li>
<li>attacking opponents - ✓</li>
<li>collecting rewards for reaching the last level-  ✗</li>
<li>repeat from 1 point - ✗</li>
</ol>
      P.S.special thanks to https://github.com/kiiiiiingdom
    </td>
  </tr>
 </table>
 
 <h3 align="center">Supported game language</h3>
<table>
  <tr>
    <td width=100vw></td>
    <td width=300vw>Russian</td>
     <td width=300vw>English</td>
    <td  width=300vw>Chinese</td>
  </tr>
  <tr>
    <td>
      3840x2160
    </td>
    <td background>
      ❌
    </td>
    <td>
      ❌
    </td>
    <td>
      ❌
    </td>
  </tr>
  <tr>
    <td>
      2560x1440
    </td>
    <td background>
      ✅
    </td>
    <td>
      ❌
    </td>
    <td>
      ❌
    </td>
  </tr>
  <tr>
    <td>
      1920x1080
    </td>
    <td>
      ❌
    </td>
    <td>
      ✅
    </td>
    <td>
      In progress
    </td>
  </tr>
 </table>

<h3 align="center">PvP system work preview</h3>

[![Watch the video](https://user-images.githubusercontent.com/68296704/137970053-fe49c896-d237-49f1-8658-46d1477340d7.png)](https://www.youtube.com/watch?v=znt1P3KkrNg&t)


The main idea of  the bot is to automatically pass the levels and assemble components, 
simultaneously pumping all your mercenaries level 1 to 30 (so far, then to add)
So how does it work?
in fact, everything is based on the fact that the bot collects a team of 3 of your heroes of level 30, 
and then throws 1 level there, and since for pumping the unit does not have to participate in the battle, 
the bot just passes the location time and time again and shakes the rest of your mercenaries to level 30.

In plans
1. Finish Project
2. Add mode selection - collecting fragments/pumping heroes
3. write a graphical interface for this whole case
4. It is possible to expand the functionality originally conceived.

<h1 align="center">Installation</h1>
<ul>
  <li>Download the project</li>
  <li>Install All Libraries</li>
</ul>
<h3 align="left">auto</h3>
<ul>
  <li>pip install -r requirements.txt</li>
</ul>
<h3 align="left">by yrself</h3>



![image](https://user-images.githubusercontent.com/68296704/137736402-fb0e7fae-5f3d-4c8d-b56e-b50ff08db56f.png)

<ul>
  <li>then open Settings.ini and set yr settings</li>
  <li>Start the game</li>
</ul>
<h1 align="center">Possible problem</h1>

![image](https://user-images.githubusercontent.com/68296704/137735448-22d49878-07b5-4bf1-b48e-0baa995f17ac.png)
<br>If this error occurs after all libraries have been installed and the interpreter has been configured, do this:
<ul>
  <li>pip install "ahk[binary]"</li>
  <li>pip install "ahk-binary<2"</li>
</ul>





<h1 align="center">Specification, Settings.ini file:</h1>
<img align="right" src="https://user-images.githubusercontent.com/68296704/137707877-189b3ca6-9981-4db8-b60d-42168c4cea7d.png"></img>


```diff
[BotSettings]
monitor=1 
bot_speed=0.5 
+0.1-the fastest mode , 5-the slowest (not recomending do faster then 0.5) 
[Hero1]
number = 1
colour = Red
[Hero2]
number = 2
colour = Green
[Hero3]
number = 3
colour = Blue
+3 main heroes that you will use for pumping other ones.List of heroes by numbers you can see in in HeroesList.txt

[NumberOfPages]
Red = 1
Green = 2
Blue = 2
+number of pages each colour(or type) in section Red - defenders , Green - warriors ,Blue - Wizards
[Resolution]
Monitor Resolution = 2560*1440
+could be 2560*1440 or 1920*1080

```

<br>
<br>
<br>
    

HeroList<br>
1 - Cariel Roame /Кариэль Роум<br>
2 -Tyrande / Тиранда<br>
3 -Milhous Manostorm / Милхаус маношторм<br>


For contacts andrey115516@gmail.com

