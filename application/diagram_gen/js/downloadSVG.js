function downloadSVG() {
    // Grab the svg by the id 
    const originalSVG = document.getElementById("timeline");

    // Get the svg source
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(originalSVG);

    // Store in blob data type
    const svgBlob = new Blob([source], {type: "image/svg+xml;charset=utf-8"});

    // Create a url of the blob
    const svgUrl = URL.createObjectURL(svgBlob);

    // Load svg onto an image
    const img = new Image();
    img.onload = function() {
        // Create a canvas to put the svg onto and then turn the vector-based image to a png
        const canvas = document.createElement("canvas");
        canvas.width = originalSVG.clientWidth || 1000;
        canvas.height = originalSVG.clientHeight || 1000;

        const context = canvas.getContext("2d");
        context.drawImage(img, 0, 0);

        canvas.toBlob((svgBlob) => {
            // Send PNG blob to server
            const formData = new FormData();
            formData.append("file", svgBlob, "Graph.png");

            fetch("http://localhost:5000/upload", {
                method: "POST",
                body: formData
            })
            .then(response => console.log("PNG upload success"))
            .catch(error => console.error("Upload failed", error));
        }, "image/png")
    };
    img.src = svgUrl;
}