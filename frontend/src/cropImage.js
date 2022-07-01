export const getCroppedImg = (image, pixelCrop, fileName) => {
    const width = (pixelCrop.width / 100) * image.naturalWidth;
    const height = (pixelCrop.height / 100) * image.naturalHeight;
    return new Promise((resolve, reject) => {
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");

        ctx.drawImage(
            image,
            (pixelCrop.x / 100) * image.naturalWidth,
            (pixelCrop.y / 100) * image.naturalHeight,
            width,
            height,
            0,
            0,
            width,
            height
        );

        // As Base64 string
        // const base64Image = canvas.toDataURL("image/jpeg");

        // As a blob

        canvas.toBlob((file) => {
            if (file) file.name = fileName;
            resolve(file);
        }, "image/jpeg");

        // resolve(dataURItoBlob(base64Image));
    });
};

function dataURItoBlob(dataURI) {
    var binary = atob(dataURI.split(",")[1]);
    var array = [];
    for (var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], { type: "image/jpeg" });
}