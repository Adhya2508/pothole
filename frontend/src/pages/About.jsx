import "../styles/about.css";

function About() {
  return (
    <div className="container about-page">

      <h1>About SmartRoad AI</h1>

      <p className="intro">
        SmartRoad AI is an AI-powered road inspection system that automatically
        detects potholes from road images using a YOLOv8 object detection model
        deployed on AWS Cloud.
      </p>

      <div className="about-card">

        <h2>🚧 Why does this matter?</h2>

        <p>
          Imagine driving on a highway at night and suddenly hitting a deep
          pothole. It damages vehicles, causes traffic congestion, and in many
          cases leads to serious accidents.
        </p>

        <p>
          Instead of waiting for someone to manually report damaged roads,
          SmartRoad AI helps identify potholes automatically from scanned road
          images. Once detected, the system can instantly notify maintenance
          authorities so repairs can begin much sooner.
        </p>

      </div>

      <div className="about-card">

        <h2>🌍 Real World Use Cases</h2>

        <ul>

          <li>🚗 Municipal corporations monitoring city roads.</li>

          <li>🛣 Highway authorities performing regular inspections.</li>

          <li>🚙 Smart vehicles collecting road images while driving.</li>

          <li>📸 Drones capturing aerial images of damaged roads.</li>

          <li>🔔 Automatic alerts sent to maintenance teams for severe potholes.</li>

          <li>📊 Building historical road condition reports for better planning.</li>

        </ul>

      </div>

      <div className="about-card">

        <h2>⚙️ How it works</h2>

        <ol>

          <li>Upload a road image.</li>

          <li>API Gateway receives the request.</li>

          <li>AWS Lambda forwards it to the EC2 inference server.</li>

          <li>YOLOv8 detects potholes.</li>

          <li>Results are stored in DynamoDB.</li>

          <li>If road damage is severe, SNS sends an email notification.</li>

          <li>The annotated image is stored in Amazon S3 and displayed back to the user.</li>

        </ol>

      </div>

    </div>
  );
}

export default About;