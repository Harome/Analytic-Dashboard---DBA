import React, { useRef, useState } from 'react';
import './about.css';
import emailjs from '@emailjs/browser';

const About = () => {
  const form = useRef();
  const [emailStatus, setEmailStatus] = useState('');

  const sendEmail = (e) => {
    e.preventDefault();

    emailjs
      .sendForm(
        'service_elgb0bh',
        'template_3r8g9o6',
        form.current,
        '_AutepQlMvHsHrna4'
      )
      .then(
        () => {
          setEmailStatus('success');
          form.current.reset();
          setTimeout(() => setEmailStatus(''), 5000); // Auto-dismiss
        },
        (error) => {
          setEmailStatus('error');
          console.error(error.text);
          setTimeout(() => setEmailStatus(''), 5000);
        }
      );
  };

  return (
    <div className="about-page-container">
      <div className="about-card">
        <h1>About Us</h1>
        <p className="justified-text-about">
          The DepEd Dashboard is a centralized data visualization platform that provides a comprehensive view of the current
          state of basic education in the Philippines. Built using official enrollment data, the dashboard presents key information
          on student population, grade-level distribution, and school presence across all regions of the country.
          Its primary goal is to make large-scale educational data easier to explore, interpret, and use for strategic planning.
        </p>
        <p className="justified-text-about">
          By turning raw data into interactive visuals, the platform offers valuable insights into how students are distributed from
          Kindergarten to Senior High School, including variations by gender, academic strand, and sector. It also helps users understand
          how schools are classified and managed, showing patterns in public and private education, as well as the concentration of
          schools in specific provinces, municipalities, and barangays.
          With these features, the dashboard helps identify which areas are underserved, where education is doing well, and where
          more support may be needed.
        </p>
        <p className="justified-text-about">
          The DepEd Dashboard is more than just a tool for viewing statistics. It is designed to support educators, policymakers,
          researchers, and the public in understanding the state of education at both local and national levels. With a focus on
          accessibility and clarity, the platform serves as a foundation for data-driven decisions that aim to improve educational
          quality, equity, and access across the Philippines.
        </p>
      </div>

      <h1 className="contact-heading">Have a question or feedback?</h1>
      <div className="contact-form-section">
        <div className="left-column">
          <p className="justified-text-contact">
            <h2 className='contact-us-text'>Contact Us!</h2>
            Thank you for visiting the DepEd Dashboard. If you have any questions, feedback, or suggestions, feel free to contact us. 
            We’re open to ideas, concerns, or inquiries to help improve the platform and make education data more accessible and useful for everyone.
          </p>
        </div>

        <div className="right-column">
          <div className="contact-card">
            <form ref={form} onSubmit={sendEmail} className="contact-form">
              <input type="text" name="user_name" placeholder="Your Name" required />
              <input type="email" name="user_email" placeholder="Your Email" required />
              <textarea name="message" placeholder="Your Message" rows="5" required></textarea>
              <button type="submit">Send Message</button>
            </form>
          </div>
        </div>
      </div>

      {emailStatus && (
        <div className="email-popup-overlay">
          <div className={`email-popup ${emailStatus}`}>
            <span className="email-popup-close" onClick={() => setEmailStatus('')}>&times;</span>
            {emailStatus === 'success' && 'Message sent successfully!'}
            {emailStatus === 'error' && 'Failed to send message. Please try again.'}
          </div>
        </div>
      )}
    </div>
  );
};

export default About;
