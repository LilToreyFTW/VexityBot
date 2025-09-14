![screenshot](http://i.imgur.com/tzMaWv4.png)
<p align="center">
  <a href="https://github.com/TSMPoke/TSMPoke-Desktop/releases/download/v2.0.0-thunderbolt/TSMPoke-2.0.0-thunderbolt-mac.zip"><img src="http://i.imgur.com/pRNJGt6.png"></a> 
  <a href="https://github.com/TSMPoke/TSMPoke-Desktop/releases/download/v2.0.0-thunderbolt/TSMPoke-2.0.0-thunderbolt-win.zip"><img src="http://i.imgur.com/CSz91B9.png"></a>
</p>
# TSMPoke - Advanced Pokemon GO Desktop Bot
**⚡ Powered by Thunderbolt Integration - The Ultimate Pokemon GO Automation Experience**

TSMPoke is an advanced desktop Pokemon GO bot featuring seamless integration with the Thunderbolt bot engine for maximum performance and reliability.

Join us at #tsmpoke channel at [our slack chat](https://pokemongo-bot.herokuapp.com/)


## ⚡ Thunderbolt Integration Features
- **Advanced Pokemon Catching**: Intelligent catching algorithms with shiny detection
- **Raid Battle Automation**: Automated raid participation with optimal team selection
- **Gym Battle System**: Strategic gym battling with team optimization
- **Real-time Statistics**: Live tracking of catches, XP, stardust, and more
- **Multiple Bot Modes**: Catching, Raiding, Battling, Exploring, and Idle modes
- **GUI Integration**: Beautiful desktop interface with real-time status updates
- **Configuration Management**: Easy bot configuration through the GUI

## Warning
 - TSMPoke is in active development. Some features may be unstable
 - Currently no linux build. Linux support is planned for future releases
 - To Linux users: Linux support is coming soon. Please be patient

## Installing from binaries
Extract the TSMPoke application from the .zip file for your platform.
Start the app and configure your Thunderbolt bot settings through the GUI.

You can also rename and move the encrypt file to the `tsmpoke` folder inside the app (windows: `resources/app/tsmpoke/encrypt.dll` / OSX: `Resources/app/tsmpoke/encrypt.so`).

### Obtaining encrypt file
You can find the pre-compiled file for your platform [here](https://github.com/PokemonGoMap/PokemonGo-Map/tree/develop/pogom/libencrypt).

### Building encrypt yourself
Run  
```
wget http://pgoapi.com/pgoencrypt.tar.gz && tar -xf pgoencrypt.tar.gz && cd pgoencrypt/src/ && make
```
Then copy `libencrypt.so` to the `gofbot` folder and rename to encrypt.so

## FAQ
Refer to [this issue](https://github.com/PokemonGoF/PokemonGo-Bot-Desktop/issues/138).

## Waffle Channel
We sync the status in [Waffle](https://waffle.io/PokemonGoF/PokemonGo-Bot-Desktop)

## Contributors
JVenberg  
ProjectBarks 
solderzzc  
JacerOmri  
ariestiyansyah  
GodLesZ  
sniok  
mmnsgo  
Outpox

*Don't forget to add yourself when doing PR*

## Credits
[PokemonGo-DesktopMap](https://github.com/mchristopher/PokemonGo-DesktopMap) Amazing job done by  Mike Christopher

## Disclaimer
©2016 Niantic, Inc. ©2016 Pokémon. ©1995–2016 Nintendo / Creatures Inc. / GAME FREAK inc. © 2016 Pokémon/Nintendo Pokémon and Pokémon character names are trademarks of Nintendo. The Google Maps Pin is a trademark of Google Inc. and the trade dress in the product design is a trademark of Google Inc. under license to The Pokémon Company. Other trademarks are the property of their respective owners.
[Privacy Policy](http://www.pokemon.com/us/privacy-policy/)

[PokemonGo-Bot](https://github.com/PokemonGoF/PokemonGo-Bot) is intended for academic purposes and should not be used to play the game *PokemonGo* as it violates the TOS and is unfair to the community. Use the bot **at your own risk**.

[PokemonGoF](https://github.com/PokemonGoF) does not support the use of 3rd party apps or apps that violate the TOS.

## Licensing
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
©2016 X Consortium

[![Analytics](https://ga-beacon.appspot.com/UA-81468120-1/desktop-welcome-page)](https://github.com/igrigorik/ga-beacon)
