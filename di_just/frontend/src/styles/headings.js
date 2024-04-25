import React from 'react';
import styled from 'styled-components';

const Heading = styled.h1`
  font-size: 36px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-top: 0;
  margin-bottom: 32px;
`;

const PrivatDigestHeading = ({ children }) => <Heading>{children}</Heading>;

export default PrivatDigestHeading;