function changeTime(time, typeArray, url_val){
    
    var val = url_val.substring(0, url_val.length-1)
    val = val + time

    $.ajax({
            url: val,
            type: 'GET',
            dataType: 'application/json',
            complete: function(data){
                data = JSON.parse(data.responseText);
                var i = 1;
                
                var shown = 0;
                var diff_display  = "Comparing latest measurement " + data.mea_id1 + " ("  + data.mea_date1 + ") with measurement "+ data.mea_id2 + " (last before " + document.getElementById("times").value + " on "+  data.mea_date2+")."
               
                $.each(data.diffs, function(key, value){
                    if(value !== null && value !== "None"){
                        const data_and_change = value.split("\t");
                        if(data_and_change[1].includes("+0.00%") ||data_and_change[1].includes("N/A")){
                            var font_color = "blue";
                            if(data_and_change[2].includes("+0.00")){
                                var second_font_color = "blue"
                            }else if (data_and_change[2].includes("+")){
                                second_font_color = "green"
                            }else{
                                second_font_color = "red"
                            }
                        }else if (data_and_change[1].includes("+")){
                            font_color = "green";
                            second_font_color = font_color
                        }else{
                            font_color = "red";
                            second_font_color = font_color
                        }
                        data_and_change[2] = data_and_change[2].fontcolor(second_font_color)
                        data_and_change[1] = data_and_change[1].fontcolor(font_color)
                        
                        document.getElementById("diff"+i).innerHTML = typeArray[i-1] + "\t" + data_and_change.join("\t")
                        
                        
                            document.getElementById("diff"+i).hidden = false;
                        
                        shown = shown+1
                        
                    }else{
                        document.getElementById("diff"+i).hidden = true;
                    }
                    if (shown === 0){
                        document.getElementById("changesDisplay").style.display = "none";
                        document.getElementById("times").hidden = true;
                        document.getElementById("timesLabel").hidden = true;
                        document.getElementById("diff display").hidden = true;
                        
                    }else if (i === 4){
                        document.getElementById("times").hidden = false;
                        document.getElementById("timesLabel").hidden = false;
                        document.getElementById("diff display").hidden = false;
                        document.getElementById("diff display").innerHTML = diff_display;
                        document.getElementById("changesDisplay").style.display = "";
                    }
                    i++
                })
                if(document.getElementById("changesDisplay").style.display === "none" && data.mea_date1 !== "None"){
                    document.getElementById("diff display").innerHTML = "No valid comparisons within the timeframe selected, try a different time?"
                    document.getElementById("times").hidden = false;
                    document.getElementById("timesLabel").hidden = false;
                    document.getElementById("diff display").hidden = false;
                    document.getElementById("changesDisplay").style.display = "";
                }
                

                

            }
        })
}

function fillSelect(){
    for(let i = 0; i<24; i++){
        let option = document.createElement("option");
        let iString = i;
        if (i<10){
            iString = "0" + iString;
        }
        option.text = iString + ":00";
        option.value = i;
        document.getElementById("times").add(option)
    }
}