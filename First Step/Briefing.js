// ==UserScript==
// @name         Briefing
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @include      https://en.wikipedia.org/wiki/List_of_ships_of_World_War_II
// @require      https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/1.3.3/FileSaver.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // ShipNames list
    var baseUri = "https://en.wikipedia.org/wiki/List_of_ships_of_World_War_II_(";
    var al = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var xhr = [];
    var GOT = 0;

    // Shiplist
    var shipList = [];

    for(var letter=0; letter < al.length; letter++){
        (function(letter){
            /* Request list page */
            xhr[letter] = new XMLHttpRequest();
            xhr[letter].open("GET", baseUri + al[letter] + ")" , true);
            xhr[letter].onreadystatechange = function(){
                /************** Single pages requests *****************************/

                // Wait for response
                if (this.readyState === 4 && this.status === 200){
                    /* DEBUG */console.log("Requesting " + baseUri + al[letter] + ")");

                    // Parse HTML
                    var page = document.createElement('html');
                    page.innerHTML = this.responseText;

                    // .getElementsByTagName("tbody")[1].getElementsByTagName("tr")
                    //     [i].getElementsByTagName("td")[0].firstChild
                    //         .href
                    //         ^ if missing raise exception
                    var letterList = page.getElementsByTagName("tbody")[1].getElementsByTagName("tr");
                    for(var ii=1; ii<letterList.length; ii++){
                        try{
                            var info = letterList[ii].getElementsByTagName("td")[0].getElementsByTagName("a")[0];
                            var shipName = info.title;
                            var shipPage = info.href // Verify existence of page
                            if(shipPage.includes("index.php")){ shipPage = "null" };
                        }catch(err){
                            shipPage = "null";
                        }
                        var data = [shipName, shipPage];
                        shipList.push(data);
                    }

                    GOT++;
                }
                /******************************************************************/
            };
            xhr[letter].send();
        })(letter);
    }

    var keep = true;

    // Interactive wait
    while(GOT < al.length && keep){
        keep = confirm("Processing: " + GOT + "/" + al.length + ", Press \"Ok\" to refresh, \"Cancel to stop\"");
    };
    if (keep){
        confirm("Got all data, beginning download");
    }

    saveAs(new Blob([JSON.stringify(shipList)],{type:'application/json;charset=utf-8'}), "listone.json");
})();