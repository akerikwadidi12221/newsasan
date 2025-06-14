import { render, screen } from '@testing-library/react';
import App from '../pages/App';

test('renders without crashing', () => {
  render(<App />);
  expect(screen.getByText(/BuildMart Online/i)).toBeInTheDocument();
});
