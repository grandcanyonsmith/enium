import "bootstrap/dist/css/bootstrap.min.css";
import "mapbox-gl/dist/mapbox-gl.css";
import "react-image-crop/dist/ReactCrop.css";
import "./App.css";
import {
  Button,
  Container,
  Form,
  Alert,
  Spinner,
  ListGroup,
} from "react-bootstrap";
import MapboxAutocomplete from "react-mapbox-autocomplete";
import { useDropzone } from "react-dropzone";
import { useRef, useMemo, useState, useEffect } from "react";
import { nanoid } from "nanoid";
import axios from "axios";
import mapboxgl from "mapbox-gl";
import { useGeolocated } from "react-geolocated";
import ReactCrop from "react-image-crop";
import { getCroppedImg } from "./cropImage";
import SelectLocation from "./SelectLocation";
import {
  faCheckCircle,
  faTimesCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

mapboxgl.accessToken =
  "pk.eyJ1IjoiY2FueW9uZnNtaXRoIiwiYSI6ImNsNHB1bnFndTA1ejgzY2xyeWswNHVzaTYifQ.xsqBneXW6U1B-N_jDzrOtg";

const baseStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "20px",
  borderWidth: 2,
  borderRadius: 2,
  borderColor: "#eeeeee",
  borderStyle: "dashed",
  backgroundColor: "#fafafa",
  color: "#bdbdbd",
  outline: "none",
  transition: "border .24s ease-in-out",
};

const focusedStyle = {
  borderColor: "#2196f3",
};

const acceptStyle = {
  borderColor: "#00e676",
};

const rejectStyle = {
  borderColor: "#ff1744",
};

const thumbsContainer = {
  display: "flex",
  flexDirection: "row",
  flexWrap: "wrap",
  marginTop: 16,
};

const thumb = {
  display: "inline-flex",
  borderRadius: 2,
  border: "1px solid #eaeaea",
  marginBottom: 8,
  marginRight: 8,
  width: "100%",
  // height: 300,
  padding: 4,
  boxSizing: "border-box",
};

const thumbInner = {
  display: "flex",
  minWidth: 0,
  overflow: "hidden",
};

const img = {
  display: "block",
  maxWidth: "100%",
};

const initCrop = {
  unit: "%",
  x: 25,
  y: 25,
  width: 50,
  height: 50,
};

const messages = {
  cropped: "ID is cropped correctly",
  blurred: "ID photo is not blurry",
  name: "ID name matches title name",
  expired: "ID is not expired",
};

function App() {
  const [crop, setCrop] = useState(initCrop);

  const [uploadProcessing, setUploadProcessing] = useState(false);
  const [file, setFile] = useState(null);
  const [croppedFile, setCroppedFile] = useState(null);
  const [selected, setSelected] = useState(null);
  const [success, setSuccess] = useState(null);
  const image = useRef();
  const [isCropping, setIsCropping] = useState(false);

  const onDrop = async (acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setCrop(initCrop);
    setIsCropping(false);
  };

  const { getRootProps, getInputProps, isFocused, isDragAccept, isDragReject } =
    useDropzone({
      accept: { "image/png": [".png", ".jpeg", ".jpg"] },
      onDrop,
      disabled: !selected,
    });
  const style = useMemo(
    () => ({
      ...baseStyle,
      ...(isFocused ? focusedStyle : {}),
      ...(isDragAccept ? acceptStyle : {}),
      ...(isDragReject ? rejectStyle : {}),
    }),
    [isFocused, isDragAccept, isDragReject]
  );

  const uploadImage = async () => {
    setUploadProcessing(true);
    setSuccess(null);

    const id = nanoid();
    const name = file.name.split(".");
    const extension = name[name.length - 1];

    let res = await fetch(
      "https://0nounobm7g.execute-api.us-east-1.amazonaws.com/dev/generate-presigned-url/" +
        id +
        "." +
        extension
    );
    res = await res.json();

    /**
     * upload file to s3
     */
    await axios.put(res.url, croppedFile, {
      headers: { "Content-Type": "image/png" },
    });

    /**
     * call api to verify
     */

    let response = await fetch(
      "https://0nounobm7g.execute-api.us-east-1.amazonaws.com/dev/verify_id_to_title/",
      {
        method: "post",
        body: JSON.stringify({
          image: `${id}.${extension}`,
          name: selected,
        }),
      }
    );
    response = await response.json();
    setSuccess(response);

    setUploadProcessing(false);
  };

  return (
    <Container>
      <Form style={{ maxWidth: "480px", margin: "20px auto" }}>
        <h4>
          Please fill out the form below to initiate a new loan application
        </h4>
        <hr></hr>
        <SelectLocation selected={selected} setSelected={setSelected} />
        <Form.Group className="mb-3">
          <Form.Label>Upload ID</Form.Label>
          <div>
            <div className="">
              <div {...getRootProps({ style })}>
                <input {...getInputProps()} />
                <p>Upload ID to verify ID matches title</p>
              </div>
              {file && (
                <aside style={thumbsContainer}>
                  <div style={thumb} key={file.name}>
                    <div style={thumbInner}>
                      <ReactCrop
                        crop={crop}
                        onChange={(c, percentCrop) => setCrop(percentCrop)}
                        onComplete={() => {
                          getCroppedImg(image.current, crop, "temp.jpg").then(
                            (v) => setCroppedFile(v)
                          );
                        }}
                        disabled={isCropping}
                      >
                        <img
                          ref={image}
                          alt="id"
                          src={URL.createObjectURL(file)}
                          style={img}
                          // Revoke data uri after image is loaded
                          onLoad={(e) => {
                            console.log(e.currentTarget.naturalHeight);
                            URL.revokeObjectURL(file.preview);
                          }}
                        />
                      </ReactCrop>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="mb-2 w-100"
                    onClick={() => {
                      if (!isCropping) {
                        setFile(croppedFile);
                        setCrop({
                          unit: "%",
                          x: 0,
                          y: 0,
                          width: 100,
                          height: 100,
                        });
                      }
                      setIsCropping(!isCropping);
                    }}
                  >
                    {isCropping ? "Crop" : "Save"}
                  </Button>
                </aside>
              )}
            </div>
          </div>
        </Form.Group>
        <Button
          className="w-100"
          onClick={uploadImage}
          disabled={
            file == null || uploadProcessing || !selected || !isCropping
          }
        >
          {uploadProcessing ? (
            <>
              <Spinner
                as="span"
                animation="grow"
                size="sm"
                role="status"
                aria-hidden="true"
                className="mr-1"
              />
              Processing...
            </>
          ) : (
            "Upload Image"
          )}
        </Button>

        {success?.success != null && (
          <Alert
            variant={success.success ? "success" : "danger"}
            className="mt-1 d-flex justify-content-between align-items-center"
          >
            <div>
              <h4>{success.message}</h4>
              {!success.success && (
                <p>
                  Contact Enium rep <a href="tel:801-555-3333">801-555-3333</a>
                </p>
              )}
            </div>
            <FontAwesomeIcon
              icon={success.success ? faCheckCircle : faTimesCircle}
              color={success.success ? "green" : "red"}
              fontSize="40px"
            />
          </Alert>
        )}
        {success?.success && (
          <Alert variant="success" className="mt-1">
            {success.message}
          </Alert>
        )}
        {success?.errors && (
          <ListGroup variant="flush">
            {Object.keys(success?.errors).map((k) => (
              <ListGroup.Item
                key={k}
                className="d-flex justify-content-between"
              >
                {messages[k]}{" "}
                <FontAwesomeIcon
                  icon={success.errors[k] ? faTimesCircle : faCheckCircle}
                  color={success.errors[k] ? "red" : "green"}
                />
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Form>
    </Container>
  );
}

export default App;
