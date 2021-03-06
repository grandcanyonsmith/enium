import "bootstrap/dist/css/bootstrap.min.css";
import "mapbox-gl/dist/mapbox-gl.css";
import { useEffect, useState } from "react";
import { Button, Form } from "react-bootstrap";
const SelectName = ({ setSelected, names, selected, namesLoading }) => {
  const [isValidName, setIsValidName] = useState(true);
  const [name, setName] = useState(null);

  useEffect(() => {
    if (selected) {
      setIsValidName(true);
    }
  }, [selected]);
  return (
    <>
      <Form.Group className="mb-3 mt-3">
        <Form.Label>Applicant Name</Form.Label>
        <div className="d-flex flex-column">
          {names.length === 0 && (
            <Button className="mt-1" variant="outline-secondary" disabled>
              {namesLoading
                ? "Loading..."
                : "Select Address above to select name"}
            </Button>
          )}
          {names?.map((v, i) => (
            <Button
              className="mt-1"
              key={i}
              variant={v.full === selected ? "primary" : "outline-primary"}
              onClick={() => {
                setSelected(v.full);
                setName(v);
              }}
            >
              {`${v.first}${v.middle ? " " + v.middle : ""} ${v.last}`}
            </Button>
          ))}
        </div>
      </Form.Group>
      <Form.Group className="mb-3 mt-3">
        <Form.Label>
          Don't see the name of the applicant ? Click{" "}
          <a
            href="#"
            onClick={(e) => {
              setIsValidName(false);
              setSelected(null);
              e.preventDefault();
            }}
          >
            here
          </a>
        </Form.Label>
        {selected && (
          <div className="d-flex flex-column mt-2">
            <div className="d-flex justify-content-between">
              <div className="px-1">
                <Form.Label>First Name</Form.Label>
                <Form.Control type="text" disabled value={name?.first} />
              </div>

              <div className="px-1">
                <Form.Label>Middle Name</Form.Label>
                <Form.Control type="text" disabled value={name?.middle} />
              </div>
            </div>
            <div className="px-1">
              <Form.Label>Last Name</Form.Label>
              <Form.Control type="text" disabled value={name?.last} />
            </div>
          </div>
        )}
      </Form.Group>
    </>
  );
};

export default SelectName;
