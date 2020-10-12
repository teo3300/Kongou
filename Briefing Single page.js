// ==UserScript==
// @name         Briefing Single page
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @include      https://en.wikipedia.org/wiki/List_of_ships_of_World_War_II_(*)
// @require      https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/1.3.3/FileSaver.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    setTimeout(function() {
        var shipDict = {};
        var done = 0, pages = 0, Null = 0, errors = 0;

        var letter = document.baseURI.substr(-2,1);
        document.getElementsByClassName("headerSort")[0].click();

        var letterList = document.getElementsByTagName("tbody")[1].getElementsByTagName("tr");
        for(var ship=0; ship<letterList.length; ship++){//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            var Entry = {
                ID:"",
                Name:"",//
                Fullname:null,
                Page:null,
                Navy:"",//
                Class:"",//
                Type:"",//
                Displacement:0,//
                Commissioned:"",//
                Fate:""//
            }
            var line = letterList[ship].getElementsByTagName("td");
            try{

                Entry.Name = line[0].innerText;
                Entry.Navy = line[1].getElementsByTagName("a")[0].title;
                Entry.Class = line[2].innerText;
                Entry.Type = line[3].innerText;
                Entry.Displacement = parseInt(line[4].innerText.split(" ")[0].replace(",",""));
                Entry.Commissioned = line[5].innerText;
                Entry.Fate = line[6].innerText;
                done ++;

                var page = line[0].getElementsByTagName("a")[0].href
                if(page.includes("index.php")){
                    Entry.Page = null;
                    Entry.Fullname = line[0].getElementsByTagName("a")[0].title.substr(0, line[0].getElementsByTagName("a")[0].title.length-22);
                }else{
                    Entry.Page = page;
                    Entry.Fullname = line[0].getElementsByTagName("a")[0].title;
                }
                pages ++;

            }catch(err){
                Entry.Page = null;
                Entry.Fullname = null;
                console.log(line[0].innerText + " ERROR: " + err);
                Null ++;
            }
            shipDict[letter + ship] = Entry;
        }
        var keep = confirm ("Done " + done + " ships of " + letterList.length + " with " + (pages + Null) + " pages (" + Null + " Missing) and " + errors + "error(s)");
        if (keep) {saveAs(new Blob([JSON.stringify(shipDict)],{type:'application/json;charset=utf-8'}), "shiplist_" + letter + "_.json");}


    }, 800);
})();