vizmap = [

    {selector: "node", css: {
	"shape": "ellipse",
	"text-valign":"center",
	"text-halign":"center",
	"content": "data(name)",
	"background-color": "#FFFFFF",
	"border-color":"black","border-width":"1px",
	"width": "mapData(degree, 0.0, 5.0, 20.0, 200.0)",
	"height":"mapData(degree, 0.0, 5.0, 20.0, 200.0)",
	"font-size":"8px"}},


    {selector: 'node[type="drug"]', css: {
	"shape": "roundrectangle",
	"font-size": "12px",
	"background-color":"#f44341"
    }},

    {selector: 'node[type="protein"]', css: {
	"shape": "roundrectangle",
	"background-color":"#4189f4",
	"font-size": "12px",
    }},

    {selector: 'node[type="disease"]', css: {
	"shape": "roundrectangle",
	"background-color":"#adf442",
    }},

    {selector: 'node[type="gene"]', css: {
	"shape": "ellipse",
    }},

    {selector: 'node[type="gene"][expression < 0]', css: {
	"background-color": "mapData(expression, -3, 0, green, white)",
	"width": "mapData(expression, -3, 0, 100, 30)",
	"height": "mapData(expression, -3, 0, 100, 30)"
    }},
    
    {selector: 'node[type="gene"][expression >=0]', css: {
	"background-color": "mapData(expression, 0, 3, white, red)",
	"width": "mapData(expression, 0, 3, 30, 100)",
	"height": "mapData(expression, 0, 3, 30, 100)"
    }},

    {selector: 'edge[type="inhibitor"]', css:{
	"line-color":"#82874e"
    }},
    {selector: 'edge[type="indication"]', css:{
	"line-color":"#87584e"
    }},
    
    {selector: 'edge[edgeType="produces"][flux < 0]', css: {
	"source-arrow-shape": "triangle",
	"source-arrow-color": "green", 
	"curve-style":"bezier",
	"line-color": "mapData(flux, -14, 0, green, #EDEDED)",
	"width":      "mapData(flux, -14, 0, 10, 1)"
    }},

    {selector: 'edge[edgeType="produces"][flux >= 0]', css: {
	"source-arrow-shape": "triangle",
	"source-arrow-color": "red", 
	"curve-style":"bezier",
	"line-color": "mapData(flux, 0, 14, #EDEDED, red)",
	"width":      "mapData(flux, 0, 14, 1, 10)"
    }},

    {selector: 'edge[edgeType="consumes"][flux < 0]', css: {
	"source-arrow-shape": "triangle",
	"source-arrow-color": "green",
	"curve-style":"bezier",
	"line-color": "mapData(flux, -14, 0, green, #EDEDED)",
	"width":      "mapData(flux, -14, 0, 10, 1)"
    }},

    {selector: 'edge[edgeType="consumes"][flux >= 0]', css: {
	"source-arrow-shape": "triangle",
	"source-arrow-color": "red", 
	"line-color": "mapData(flux, 0, 14, #EDEDED, red)",
	"width":      "mapData(flux, 0, 14, 1, 10)",
	"curve-style":"bezier"   // bezier, haystack
    }},


    {selector: 'edge[edgeType="catalyzes"]', css: {
	"line-color": "black",
	"target-arrow-shape": "circle",
	"target-arrow-color": "rgb(102, 102, 102)",
	width: "1px",
	"curve-style":"bezier"
    }},

    {selector:"node:selected", css: {
	"text-valign":"center",
	"text-halign":"center",
	//"content": "data(id)",
	"border-color": "black",
	"overlay-opacity": 0.2,
	"overlay-color": "gray"
    }},
    
    {selector:"edge:selected", css: {
	"overlay-opacity": 0.2,
	"overlay-color": "red"
    }}
];
