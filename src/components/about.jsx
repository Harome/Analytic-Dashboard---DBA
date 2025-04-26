import React, { useRef } from 'react';
import './about.css';
import emailjs from '@emailjs/browser';

const About = () => {
  const form = useRef();

  const sendEmail = (e) => {
    e.preventDefault();

    emailjs
      .sendForm(
        'your_service_id',     // Replace with your actual service ID
        'your_template_id',    // Replace with your actual template ID
        form.current,
        'your_public_key'      // Replace with your actual public key
      )
      .then(
        (result) => {
          alert('Feedback sent successfully!');
          form.current.reset();
        },
        (error) => {
          alert('Failed to send feedback. Please try again.');
          console.log(error.text);
        }
      );
  };

  return (
    <div className="about-container">
      <div className="profile-section">
        <img
          src="https://via.placeholder.com/150"
          alt="Profile"
          className="profile-image"
        />
        <h1 className="name">Hi, I'm Jane Doe</h1>
        <p className="title">Frontend Developer & UI/UX Designer</p>
      </div>

      <div className="bio-section">
        <p>
          I'm a passionate developer focused on crafting clean and user-friendly interfaces.
        </p>
        <p>
          Let’s build something great together!
        </p>
      </div>

      <form ref={form} onSubmit={sendEmail} className="feedback-form">
        <h2>Send Me Your Feedback</h2>
        <input type="text" name="user_name" placeholder="Your Name" required />
        <input type="email" name="user_email" placeholder="Your Email" required />
        <textarea name="message" placeholder="Your Feedback" required></textarea>
        <button type="submit">Send Feedback</button>
      </form>
    </div>
  );
};

export default About;
