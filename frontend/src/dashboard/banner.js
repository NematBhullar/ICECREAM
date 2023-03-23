import React from "react";

function Banner(props) {
  return (
    <div style={{ ...bannerStyle, ...myCenterElement }}>
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

const myCenterElement = {
  position: "fixed",
  left: "50vw",
  top: "6.5vh",
  transform: "translate(-50%, -50%)",
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
