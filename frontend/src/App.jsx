import "bootstrap/dist/css/bootstrap.min.css";
import "mapbox-gl/dist/mapbox-gl.css";
import { Container, Form } from "react-bootstrap";
import "./App.css";
import IncomeVerification from "./income-verification/IncomeVerification";
import TitleVerification from "./title-verification/TitleVerification";

function App() {
  return (
    <Container>
      <Form style={{ maxWidth: "480px", margin: "20px auto" }}>
        <h4>
          Please fill out the form below to initiate a new loan application
        </h4>
        <hr></hr>
        <TitleVerification />
        <hr></hr>
        <IncomeVerification />
      </Form>
    </Container>
  );
}

export default App;
