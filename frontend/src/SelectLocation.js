import "bootstrap/dist/css/bootstrap.min.css";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { useEffect, useRef, useState } from "react";
import { Button, Form, Alert } from "react-bootstrap";
import { useGeolocated } from "react-geolocated";
import "react-image-crop/dist/ReactCrop.css";
import MapboxAutocomplete from "react-mapbox-autocomplete";
import SelectName from "./SelectName";

const SelectLocation = ({ selected, setSelected }) => {
  const { coords, isGeolocationEnabled } = useGeolocated({
    positionOptions: {
      enableHighAccuracy: false,
    },
    userDecisionTimeout: 5000,
  });

  const map = useRef(null);
  const marker = useRef(null);
  const popup = useRef(null);
  const mapContainer = useRef(null);
  const [lng, setLng] = useState(-70.9);
  const [lat, setLat] = useState(42.35);
  const [selectLocation, setSelectLocation] = useState(null);
  const [names, setNames] = useState([]);
  const [namesLoading, setNamesLoadings] = useState(false);
  const [address, setAddress] = useState(null);
  const [isLocationCorrect, setIsLocationCorrect] = useState(null);
  const [streetView, setStreetView] = useState(null);

  useEffect(() => {
    if (map.current) return;
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/satellite-streets-v11",
      center: [lng, lat],
      zoom: 17,
    });
  });

  useEffect(() => {
    if (map.current && selectLocation) {
      popup.current?.remove();
      marker.current?.remove();

      map.current.setCenter([lng, lat - 0.5]);
      marker.current = new mapboxgl.Marker()
        .setLngLat([lng, lat])
        .addTo(map.current);

      popup.current = new mapboxgl.Popup({
        offset: 35,
        closeButton: false,
        closeOnClick: false,
      }) // add popups
        .setLngLat([lng, lat])
        .setHTML(
          `<div>
          <h6 style="font-size:14px">Application Location</h6><p>${selectLocation}</p>
          ${streetView ? `<img class="w-100" src='${streetView}' />` : null}
          
          </div>`
        )
        .addTo(map.current);
    } else {
      popup.current?.remove();
      marker.current?.remove();
    }
  }, [lat, lng, selectLocation, streetView]);

  useEffect(() => {
    if (!isLocationCorrect) {
      setSelected(null);
    }
  }, [isLocationCorrect]);

  useEffect(() => {
    if (isGeolocationEnabled && coords && map.current) {
      map.current.setCenter([coords.longitude, coords.latitude]);
      new mapboxgl.Marker()
        .setLngLat([coords.longitude, coords.latitude])
        .addTo(map.current);

      new mapboxgl.Popup({
        offset: 35,
        closeButton: false,
        closeOnClick: false,
      }) // add popups
        .setLngLat([coords.longitude, coords.latitude])
        .setHTML(`<div><h6 style="font-size:14px">Current Location</h6></div>`)
        .addTo(map.current);
    }
  }, [coords, isGeolocationEnabled]);

  const suggestionSelect = (result, lat, lng, text) => {
    const streetViewUrl = `https://maps.googleapis.com/maps/api/streetview?size=250x100&location=${lat},${lng}&fov=80&heading=70&pitch=0&key=AIzaSyDt02hklCJb9re6Q3Xi1WMAXRMN_l9_PXo&return_error_code=true`;
    fetch(streetViewUrl).then((res) => {
      if (res.status === 404) {
        setStreetView(null);
      } else {
        setStreetView(streetViewUrl);
      }
    });
    setSelectLocation(result);
    setIsLocationCorrect(null);

    setLat(lat);
    setLng(lng);
    const addr = result.split(", ");

    const stateAndZip = addr[addr.length - 2].split(" ");
    const zip = stateAndZip[stateAndZip.length - 1];
    const state = stateAndZip.slice(0, -1).join(" ").toLowerCase();
    const city = addr[addr.length - 3].toLowerCase();
    let street = "";
    if (addr.length > 3) street = addr[0].toLowerCase();

    setAddress({
      street,
      city,
      zip,
      state,
    });

    setNamesLoadings(true);
    setNames([]);
    setSelected(null);
    fetch(
      "https://0nounobm7g.execute-api.us-east-1.amazonaws.com/dev/getName",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          street,
          city,
          zip,
          state,
        }),
      }
    )
      .then((res) => res.json())
      .then((res) => {
        setNamesLoadings(false);
        if (res.name?.length > 0) {
          setNames(res.name);
        } else setNames([]);
      });
  };

  return (
    <>
      <Form.Group className="mb-3">
        <Form.Label>Address</Form.Label>
        <MapboxAutocomplete
          publicKey="pk.eyJ1IjoiY2FueW9uZnNtaXRoIiwiYSI6ImNsNHB1bnFndTA1ejgzY2xyeWswNHVzaTYifQ.xsqBneXW6U1B-N_jDzrOtg"
          inputClass="form-control search"
          onSuggestionSelect={suggestionSelect}
          country="us"
          resetSearch={false}
        />
      </Form.Group>
      <div ref={mapContainer} className="map-container" />

      {selectLocation && (
        <Form.Group className="mb-3 mt-3">
          <Form.Label>Is this the correct location ?</Form.Label>
          <div className="d-flex flex-column mb-3">
            <Button
              className="mt-1"
              variant={isLocationCorrect ? "primary" : "outline-primary"}
              onClick={() => {
                setIsLocationCorrect(true);
              }}
            >
              Yes
            </Button>
            <Button
              className="mt-1"
              variant={
                !isLocationCorrect && isLocationCorrect != null
                  ? "primary"
                  : "outline-primary"
              }
              onClick={() => {
                setIsLocationCorrect(false);
              }}
            >
              No
            </Button>
          </div>
          {isLocationCorrect ? (
            <div className="d-flex flex-column address">
              <div className="d-flex justify-content-between">
                <div className="px-1">
                  <Form.Label>Address</Form.Label>
                  <Form.Control disabled type="text" value={address?.street} />
                </div>
                <div className="px-1">
                  <Form.Label>City</Form.Label>
                  <Form.Control disabled type="text" value={address?.city} />
                </div>
              </div>
              <div className="d-flex justify-content-between mt-2">
                <div className="px-1">
                  <Form.Label>State</Form.Label>
                  <Form.Control disabled type="text" value={address?.state} />
                </div>
                <div className="px-1">
                  <Form.Label>Zip</Form.Label>
                  <Form.Control disabled type="text" value={address?.zip} />
                </div>
              </div>
            </div>
          ) : isLocationCorrect !== null ? (
            <Alert variant="danger" className="mt-1">
              <p>Please re-enter the correct location</p>
            </Alert>
          ) : null}
        </Form.Group>
      )}

      {isLocationCorrect && (
        <SelectName
          selected={selected}
          names={names}
          namesLoading={namesLoading}
          setSelected={setSelected}
        />
      )}
    </>
  );
};

export default SelectLocation;
