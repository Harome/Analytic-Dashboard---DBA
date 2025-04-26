import React, { useRef } from 'react';
import './about.css';
import emailjs from '@emailjs/browser';

const About = () => {
  const form = useRef();

  const sendEmail = (e) => {
    e.preventDefault();

    emailjs
      .sendForm(
        'service_elgb0bh',   // <-- replace this with your actual EmailJS Service ID
        'template_3r8g9o6',  // <-- replace this with your actual EmailJS Template ID
        form.current,
        '_AutepQlMvHsHrna4'    // <-- replace this with your actual EmailJS Public Key
      )
      .then(
        () => {
          alert('Message sent successfully!');
          form.current.reset();
        },
        (error) => {
          alert('Failed to send message. Please try again.');
          console.error(error.text);
        }
      );
  };

  return (
    <div className="about-page-container">
      <div className="about-card">
        <h1>About Us</h1>
        <p className="justified-text-about">
          The DepEd Dashboard is a centralized data visualization platform that provides a comprehensive view of the current state of basic education in the Philippines. Built using official enrollment data, the dashboard presents key information on student population, grade-level distribution, and school presence across all regions of the country. 
          Its primary goal is to make large-scale educational data easier to explore, interpret, and use for strategic planning.
        </p>
        <p className="justified-text-about">
          By turning raw data into interactive visuals, the platform offers valuable insights into how students are distributed from Kindergarten to Senior High School, including variations by gender, academic strand, and sector. It also helps users understand how schools are classified and managed, showing patterns in public and private education, as well as the concentration of schools in specific provinces, municipalities, and barangays. 
          With these features, the dashboard helps identify which areas are underserved, where education is doing well, and where more support may be needed.
        </p>
        <p className="justified-text-about">
          The DepEd Dashboard is more than just a tool for viewing statistics. 
          It is designed to support educators, policymakers, researchers, and the public in understanding the state of education at both local and national levels. With a focus on accessibility and clarity, the platform serves as a foundation for data-driven decisions that aim to improve educational quality, equity, and access across the Philippines.
        </p>
      </div>

      <div className="contact-card">
        <h2>Contact Us</h2>
        <p className="justified-text-contact">
          Thank you for visiting the DepEd Dashboard. If you have any questions, feedback, or suggestions, feel free to contact us. We’re open to ideas, concerns, or inquiries to help improve the platform and make education data more accessible and useful for everyone.
        </p>
        <form ref={form} onSubmit={sendEmail} className="contact-form">
          <input type="text" name="user_name" placeholder="Your Name" required />
          <input type="email" name="user_email" placeholder="Your Email" required />
          <textarea name="message" placeholder="Your Message" rows="5" required></textarea>
          <button type="submit">Send Message</button>
        </form>
      </div>
    </div>
  );
};

export default About;
