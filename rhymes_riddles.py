#  gcompris - rhymes_riddles.py
#
# Copyright (C) 2003, 2008 Bruno Coudoin | Srishti Sethi
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# rhymes_riddles activity.
import gtk
import gtk.gdk
import gcompris
import gcompris.utils
import gcompris.skin
import gcompris.bonus
import goocanvas
import pango
import random
import string
from BrailleMap import *
from BrailleChar import *
from gcompris import gcompris_gettext as _

#Constants Declaration
COLOR_ON = 0XCC3399L
COLOR_OFF = 0X00000000L
CIRCLE_FILL = "#CC3399"
CIRCLE_STROKE = "black"
CELL_WIDTH = 30
RHYMES_RIDDLES_LIST = [
      [ # Level 1
      [_("What goes up white and comes down yellow and white?"),"egg"],
      [_("What rises and waves all day?"),"flag"],
      [_("What has two wheels and speeds up hills for a hike?"),"bike"],
      [_("What hides in shoes and crosses the street?"),"feet"],
      [_("What falls from the sky without hurting your brain?"),"rain"]
      ],
      [# Level 2
  [_("This is a word which rhymes with cat, It grows on your head because it's a :"),"hat"],
  [_("I'm useful for journey when you are going far, I need lots of petrol because I'm a :"),"car"],
  [_("This is a word which rhymes with up.You can drink out of me because I'm a :"),"cup"],
  [_("This is a word which rhymes with bake, I'm nice to eat because I'm a : "),"cake"],
  [_("This is a word which rhymes with spoon, I shine at night because I'm a :"),"moon"]
  ],
  [# Level 3
  [_("A never ending circle,a brightly shiny thing,It's on my fourth finger because its a :"),"ring"],
  [_("The more I dry,The wetter I get"),"towel"],
  [_("What has roots as nobody sees, Is taller than trees,up it goes and yet never grows"),"mountain"],
  [_("You hear my sound you feel me when I move,But see me when you never will"),"wind"],
  [_("You'll find us near ponds or sitting on logs, we jump and we cloak because we are : "),"frogs"]
  ],
 [# Level 4
  [_("What do you get when you put a car and a pet together?"),"carpet"],
  [_("What can speak in every language , but never went to school ?"),"echo"],
  [_("What's expensive and floats through the room?"),"perfume"],
  [_("What got loose and spoiled the race"),"shoelace"],
  [_("Some fly, some sting, some hide in rugs"),"bugs"]
  ]
]
class Gcompris_rhymes_riddles:
  """Empty gcompris python class"""


  def __init__(self, gcomprisBoard):

    # Save the gcomprisBoard, it defines everything we need
    # to know from the core
    self.gcomprisBoard = gcomprisBoard
    self.gcomprisBoard.level=1
    self.gcomprisBoard.sublevel=1
    self.gcomprisBoard.number_of_sublevel=1
    self.gcomprisBoard.maxlevel = 4

    self.counter = 0
    # These are used to let us restart only after the bonus is displayed.
    # When the bonus is displayed, it call us first with pause(1) and then with pause(0)
    self.board_paused  = 0
    self.gamewon       = 0

    #Boolean variable declaration
    self.mapActive = False

    # Needed to get key_press
    gcomprisBoard.disable_im_context = True

    for index in range(4):
        random.shuffle(RHYMES_RIDDLES_LIST[index])

  def start(self):
    # Set the buttons we want in the bar
    gcompris.bar_set(gcompris.BAR_LEVEL)
    gcompris.bar_location(300,-1,0.6)
    gcompris.bar_set_level(self.gcomprisBoard)

    # Set a background image
    gcompris.set_default_background(self.gcomprisBoard.canvas.get_root_item())
    gcompris.set_background(self.gcomprisBoard.canvas.get_root_item(),
                            "rhymes_riddles/riddle.jpg")
    gcompris.set_cursor(gcompris.CURSOR_SELECT)

    #REPEAT ICON
    gcompris.bar_set(gcompris.BAR_LEVEL|gcompris.BAR_REPEAT_ICON)
    gcompris.bar_location(300,-1,0.6)

    # Create our rootitem. We put each canvas item in it so at the end we
    # only have to kill it. The canvas deletes all the items it contains
    # automaticaly.
    self.rootitem = goocanvas.Group(parent =
                                    self.gcomprisBoard.canvas.get_root_item())

    self.display_game(self.gcomprisBoard.level)


  def display_game(self,level):
      if(level == 1 or level == 2 or level == 3 or level == 4):
          self.rhymes_rhymes(level)

  def rhymes_rhymes(self, level):
      goocanvas.Text(parent = self.rootitem,
                   x=270.0,
                   y=270.0,
                   text=RHYMES_RIDDLES_LIST[level - 1][self.counter][0],
                   fill_color="black",
                   anchor = gtk.ANCHOR_CENTER,
                   alignment = pango.ALIGN_CENTER,
                   width = 500 ,
                   font = 'SANS 17'
                   )
      str = RHYMES_RIDDLES_LIST[level - 1][self.counter][1]
      for index in range(len(str)):
          BrailleChar(self.rootitem,index*(CELL_WIDTH+20)+100,350,40,str[index],
                      COLOR_ON, COLOR_OFF, CIRCLE_FILL,
                      CIRCLE_FILL, False, False, True,None)

      # the answer area
      self.entry = gtk.Entry()
      self.entry.connect("activate", self.enter_callback,self.entry,level)

      goocanvas.Widget(
                       parent = self.rootitem,
                       widget=self.entry,
                       x = 100,
                       y = 300,
                       width = 170,
                       height= 300,
                       anchor=gtk.ANCHOR_NW)
      if(level  == 1 and self.counter == 0):
          self.entry.set_text(_("Type your answer here"))
      else :
          self.entry.set_text("")


  def enter_callback(self,widget, entry, level):
      if(string.lower(self.entry.get_text()) ==
          RHYMES_RIDDLES_LIST[level - 1][self.counter][1]):
          self.gamewon = 1
          gcompris.bonus.display(gcompris.bonus.WIN,gcompris.bonus.FLOWER)
      else:
          self.gamewon = 0
          gcompris.bonus.display(gcompris.bonus.LOOSE,gcompris.bonus.FLOWER)

  def end(self):
    # Remove the root item removes all the others inside it
    self.rootitem.remove()


  def ok(self):
    print("rhymes_riddles ok.")


  def repeat(self):
    if(self.mapActive):
          self.end()
          self.start()
          self.mapActive = False
          self.pause(0)
    else :
          self.rootitem.props.visibility = goocanvas.ITEM_INVISIBLE
          self.rootitem = goocanvas.Group(parent=
                                   self.gcomprisBoard.canvas.get_root_item())
          gcompris.set_default_background(self.gcomprisBoard.canvas.get_root_item())
          map_obj = BrailleMap(self.rootitem, COLOR_ON, COLOR_OFF, CIRCLE_FILL, CIRCLE_STROKE)
          self.mapActive = True
          self.pause(1)

  def config(self):
    print("rhymes_riddles config.")


  def key_press(self, keyval, commit_str, preedit_str):
    utf8char = gtk.gdk.keyval_to_unicode(keyval)
    strn = '%c' % utf8char

  def pause(self, pause):
      self.board_paused = pause
      if(self.board_paused == 0) and (self.gamewon == 1):
          self.gamewon = 0
          self.counter +=1
          if(self.counter == 5):
              self.increment_level()
          self.end()
          self.start()
      # There is a problem with GTK widgets, they are not covered by the help
      # We hide/show them here
      if(self.board_paused):
          self.entry.hide()
      else :
          self.entry.show()


  def set_level(self, level):
    gcompris.sound.play_ogg("sounds/receive.wav")
    self.gcomprisBoard.level = level
    self.gcomprisBoard.sublevel = 1
    gcompris.bar_set_level(self.gcomprisBoard)
    self.end()
    self.start()

  def increment_level(self):
    self.counter = 0
    gcompris.sound.play_ogg("sounds/bleep.wav")
    self.gcomprisBoard.sublevel += 1
    if(self.gcomprisBoard.sublevel>self.gcomprisBoard.number_of_sublevel):
        self.gcomprisBoard.sublevel=1
        self.gcomprisBoard.level += 1
        if(self.gcomprisBoard.level > self.gcomprisBoard.maxlevel):
            self.gcomprisBoard.level = 1
