import UploadCard from '../components/UploadCard'
import '../styles/home.css'

function Home() {
  return (
    <div className="home">
      <div className="container">
        <section className="hero">
          <h1>AI Powered Road Damage Detection</h1>
          <p>Detect potholes instantly using YOLOv8 deployed on AWS Cloud.</p>
        </section>

        <UploadCard />
      </div>
    </div>
  )
}

export default Home