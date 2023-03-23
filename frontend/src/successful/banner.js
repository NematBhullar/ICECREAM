import React from "react";

function Banner(props) {
  return (
    <div style={bannerStyle}>
      <div style={logoPositionStyle}>
        <img
          style={bannerLogoStyle}
          alt="Icecream logo"
          src="https://www.elephantasticvegan.com/wp-content/uploads/2020/06/vegan-mango-ice-cream-3.jpg.webp"
        />
      </div>
    </div>
  );
}

const bannerStyle = {
  width: "100vw",
  height: "13vh",
  backgroundColor: "#23346F",
  color: "#23346F",
};

const bannerLogoStyle = {
  position: "fixed",
  objectFit: "cover",
  borderRadius: "50vh",
  height: "10vh",
  width: "10vh",
};

const logoPositionStyle = {
  position: "fixed",
  top: "1.5vh",
  left: "1vw",
};

export default Banner;
