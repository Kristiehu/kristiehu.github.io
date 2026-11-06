// ─────────────────────────────────────────────────────────────
// Data for the Teaching & Service page (src/pages/teaching.astro).
// Add a term, a course or a role here; the page layout updates itself.
// Empty sections are hidden automatically.
// ─────────────────────────────────────────────────────────────

export type Role = {
	role: string;
	org: string; // [text](https://…) makes a link
	start: string;
	end?: string; // leave out for a one-off role; use 'present' for ongoing
	points?: string[]; // [text](https://…) makes a link
};

// Shown under the heading "Leadership & Service" (set in src/pages/teaching.astro).
// LEADERSHIP is a name used in the code: no spaces or & allowed.
export const LEADERSHIP: Role[] = [
	{
		role: 'Project Review Committee',
		org: '[Graduate Studies Endowment Fund](https://uwaterloo.ca/graduate-studies-endowment-fund/), University of Waterloo',
		start: 'Nov 2026',
		end: 'present',
		points: [
        	'Review small and large project funding proposals to support graduate student initiatives.',
        	'Participate in committee discussions and project presentations to evaluate and recommend funding decisions.',
        ],
	},
	{
		role: 'Program Committee',
		org: '[AAAI-27 SA](https://aaai.org/conference/aaai/aaai-27/), Association for the Advancement of Artificial Intelligence (AAAI) 2027, Montréal, Canada',
		start: 'Oct 2026',
		end: 'present',
		points: [
        	'Review research submissions to the AAAI-27 Student Abstract Program.',
        	'Contribute to the peer-review process for work presented at AAAI-27 in Montréal, Canada (Feb 16–23, 2027).',
      	],
	},
	{
		role: 'Vice President',
		org: 'Civil & Environmental Engineering Graduate Association (CE²GA), University of Waterloo',
		start: 'Sep 2026',
		end: 'present',
		points: [
			'Plan academic, social and student-support events with the executive team through biweekly meetings.',
			'Created and run the [CE²GA LinkedIn page](https://www.linkedin.com/company/civil-and-environmental-engineering-graduate-student-association-ce2ga/) to promote events and connect graduate students with industry.',
		],
	},
	{
		role: 'Ambassador',
		org: 'ISPRS Student and Early Professionals (ISPRS STEP)',
		start: 'Sep 2026',
		end: 'present',
		points: ['Support the organisation of ISPRS conferences, congresses and symposia.'],
	},
];

export type Course = {
	code: string;
	title: string;
	roles?: string[]; // e.g. ['Teaching Assistant', 'Guest lecture']
	tasks?: string[]; // e.g. ['Labs', 'Grading']
	terms?: string[]; // e.g. ['F22', 'W23'] (shown when filled in)
};

export type Institution = {
	institution: string;
	role?: string;
	courses: Course[];
};

// Courses you have taken (PhD coursework). Leave empty to hide the section.
// Example: { code: 'CIVE 700', title: 'Course title', term: 'F26' }
export const COURSEWORK: { code: string; title: string; term?: string }[] = [
	// Hidden since Oct 2026. Uncomment a line to show the section again.
	// { code: 'GEOG 600', title: 'Foundations in Spatial Data Handling', term: 'Fall 2022' },
	// { code: 'GEOG 675', title: 'Selected Topics in Geography: LiDAR Remote Sensing', term: 'Fall 2022' },
	// { code: 'GEOG 700', title: 'Professional Skills Development for Master Students', term: 'Fall 2022' },
	// { code: 'SYDE 770', title: 'Selected Topics in Communication and Information: Remote Sensing Systems', term: 'Winter 2023' },
	// { code: 'CIVE 705', title: 'Subsurface Energy Storage Review', term: 'Fall 2026' },
];
