import React from 'react';
import styled from 'styled-components';

const StyledBody = styled.body`
  background: radial-gradient(circle at 3% 10%, #00bfff, #010124);
  background-size: 100% 200%;
  background-position: 50% 0%;
  background-repeat: no-repeat;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  animation: gradient 3s ease infinite;
`;

const Tastemaker = () => {
  return (
    <StyledBody>
      {/* Your content goes here */}
    </StyledBody>
  );
};

export default Tastemaker;