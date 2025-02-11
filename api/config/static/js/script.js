const buttons_tabel_maker = document.querySelectorAll("button.TableMaker");

for (const btn of buttons_tabel_maker){
    btn.addEventListener("mousedown", async(event) => {
        
       /*
        fetch(btn.dataset.to)
	    .then(res => {
	        const disposition = res.headers.get('Content-Disposition');
	        filename = disposition.split(/;(.+)/)[1].split(/=(.+)/)[1];
	        if (filename.toLowerCase().startsWith("utf-8''"))
	            filename = decodeURIComponent(filename.replace("utf-8''", ''));
	        else
	            filename = filename.replace(/['"]/g, '');
	        return res.blob();
	    })
	    .then(blob => {
	        var url = window.URL.createObjectURL(blob);
	        var a = document.createElement('a');
	        a.href = url;
	        a.download = filename;
	        document.body.appendChild(a); // append the element to the dom
	        a.click();
	        a.remove(); // afterwards, remove the element  
	    });
	    */
	    var url = "table_maker_3.xlsx";
	    var filename = "table_maker_3.xlsx";
	    var a = document.createElement('a');
	    var div = document.getElementById("download_label")
        a.href = url;
        a.download = filename;
        var name = btn.innerHTML;
        a.innerHTML = `${name}`;
        //document.body.appendChild(a); // append the element to the dom
        div.append(a);
        a.click();
        // afterwards, remove the element
    
    });

}