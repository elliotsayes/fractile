// This function will run after the Google Maps API has finished leading,
// as specified by the &callback=initMap parameter in the Maps API script
// URL (below).
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: 0, lng: 0},
        zoom: 2,
        streetViewControl: false,
        mapTypeControlOptions: {
            mapTypeIds: ["mandelbrot", "julia"],
        },
    });

    const mandelbrotMapType = new google.maps.ImageMapType({
        getTileUrl: function (coord, zoom) {
            const normalizedCoord = getNormalizedCoord(coord, zoom);

            if (!normalizedCoord) {
                return "";
            }
            // const bound = Math.pow(2, zoom);
            return (
                "api/tiles/mandelbrot/" +
                zoom +
                "/" +
                normalizedCoord.x +
                "/" +
                normalizedCoord.y +
                "/" +
                "tile.png"
            );
        },
        tileSize: new google.maps.Size(256, 256),
        maxZoom: 30,
        minZoom: 2,
        radius: 1738000,
        name: "Mandelbrot Set",
    });

    const juliaMapType = new google.maps.ImageMapType({
        getTileUrl: function (coord, zoom) {
            const normalizedCoord = getNormalizedCoord(coord, zoom);

            if (!normalizedCoord) {
                return "";
            }
            // const bound = Math.pow(2, zoom);
            return (
                "api/tiles/julia/" +
                zoom +
                "/" +
                normalizedCoord.x +
                "/" +
                normalizedCoord.y +
                "/" +
                "tile.png"
            );
        },
        tileSize: new google.maps.Size(256, 256),
        maxZoom: 30,
        minZoom: 2,
        radius: 1738000,
        name: "Julia Set",
    });

    map.mapTypes.set("mandelbrot", mandelbrotMapType);
    map.mapTypes.set("julia", juliaMapType);
    map.setMapTypeId("mandelbrot");

    let infoWindow = new google.maps.InfoWindow();

    map.addListener("click", (mapsMouseEvent) => {
        infoWindow.close();

        infoWindow = new google.maps.InfoWindow({
            position: mapsMouseEvent.latLng,
        });

        let latlng = mapsMouseEvent.latLng.toJSON();
        console.log(latlng);
        let latlng_str = JSON.stringify(latlng, null, 2);
        let complex_str = getComplexCoordinateStr(latlng)

        infoWindow.setContent(complex_str);
        infoWindow.open(map);
    });
}

function getComplexCoordinateStr(coord) {
    let lng = coord.lng
    let lat = coord.lat

    const scale = 4;
    let real = scale * (lng / 180);
    let imag = scale * (Math.log(Math.tan(Math.PI/4 + lat * (Math.PI / 180) / 2)) / Math.PI);

    let separator = imag < 0 ? " - " : " + ";

    const dp = 10
    return real.toFixed(dp) + separator + Math.abs(imag).toFixed(dp) + "im"
}

// Normalizes the coords that tiles repeat across the x axis (horizontally)
// like the standard Google map tiles.
function getNormalizedCoord(coord, zoom) {
    let y = coord.y;
    let x = coord.x;
    // tile range in one direction range is dependent on zoom level
    // 0 = 1 tile, 1 = 2 tiles, 2 = 4 tiles, 3 = 8 tiles, etc
    const tileRange = 1 << zoom;

    // don't repeat across y-axis (vertically)
    if (y < 0 || y >= tileRange) {
        return null;
    }

    // repeat across x-axis
    if (x < 0 || x >= tileRange) {
        x = ((x % tileRange) + tileRange) % tileRange;
    }
    return {x: x, y: y};
}