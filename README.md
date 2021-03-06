# MentorMatching

## Project Description

* #### Mentor Matching

The goal is to match students working on CS related projects to mentors that best meet the requirements of such a project.

We first compute a similarity score between each (mentor, student) pair - at the moment this is a Jaccard Similarity score but I will provide additional scoring options. We then rank the mentors in decending order (from most similar to least similar) for each student. We greedily pick the (student, mentor) pair with the highest similarity. Once a mentor has reached his/her student capacity, this mentor becomes unavailable. The process continues until every student is matched to exactly one mentor.

* #### Big and Littles

The goal is to match incoming CS freshmen to sophomores, juniors, or seniors with similar interests or club memberships.

We first compute a similarity score between each (mentor, student) pair - at the moment this is a Jaccard Similarity score weighted by the number of classes taken by the mentor, but I will provide additional scoring options. We then rank the mentors in decending order (from most similar to least similar) for each student. We greedily pick the (student, mentor) pair with the highest similarity. Once a mentor has reached his/her student capacity, this mentor becomes unavailable. The process continues until every student is matched to exactly one mentor.

## List of functions

* ### StudentSimilarityMentor(allstudents, allcoaches, t, tupleBinary)

#### Description

Returns a dataframe where each column i is the set of all mentors in decreasing order of similarity to the given student i.

#### Parameters

**allstudents** is the dataframe of all the students.

**allcoaches** is the dataframe of all the mentors/coaches

(**Note**: These must be in the format of the survey sent out but you can easily modify the parts of the code where features are extracted if this format changes.)

**t** is a parameter that takes in three (for now) values that express the type of similarity to be used: 'sl', 's', 'l'. Where 'sl' means Skill & Languages, 's' is Skills only, 'l' is Languages only.

**tupleBinary** is a binary parameter. If given 0 it will return a dataframe with only the names of the mentors. If given 1 it will return a dataframe of the names and similarity scores joined together by a '#' symbol.


* ### MenteeSimilarityMentor(allmentees, allmentors, t, tupleBinary)

#### Description

Returns a dataframe where each column i is the set of all mentors in decreasing order of similarity to the given student i.

#### Parameters

**allmentees** is the dataframe of all freshman mentees.

**allmentors** is the dataframe of all the student mentors

(**Note**: These must be in the format of the survey sent out but you can easily modify the parts of the code where features are extracted if this format changes.)

**t** is a parameter that takes in three (for now) values that express the type of similarity to be used: 'ic', 'i', 'c'. Where 'sl' means Interest & Clubs, 'i' is Interests only, 'c' is Clubs only.

**tupleBinary** is a binary parameter. If given 0 it will return a dataframe with only the names of the mentors. If given 1 it will return a dataframe of the names and similarity scores joined together by a '#' symbol.


* ### MentorPreferences(allcoaches, allstudents)

#### Description

Each mentor was asked which of the student projects they would be interested in mentoring. This function returns a dataframe of which students each mentor is willing to work with.

#### Parameters

**allstudents** is the dataframe of all the students.

**allcoaches** is the dataframe of all the mentors/coaches

* ### FeasibleMatching(studentPreferences, mentorPreferences)

#### Description

Returns a dataframe of matchings that intersect the mentorpreference dataframe and are ordered based students preferences

#### Parameters

**studentPreferences** is the dataframe returned by StudentSimilarityMentor()

**mentorPreferences** is the dataframe returned by the MentorPreferences()

* ### match1(studentpreferences, allcoaches, t)

#### Description

Returns a dataframe of (student, mentor) pairs picking from left to right and top to bottom

#### Parameters

**studentpreferences** is the dataframe returned by StudentSimilarityMentor()

**allcoaches** is all the dataframe of all the mentors/coaches

**t** is the capacity of mentors (if t=1 every student is matched to a distinct mentor)

* ### match2(studentpreferences, allcoaches, t)

#### Description

Returns a matching of (student, mentor) pairs picking greedily based on the similarity score

#### Parameters

**studentpreferences** is the dataframe returned by StudentSimilarityMentor() - note: the tupleBinary parameter must be 1 here

**allcoaches** is all the dataframe of all the mentors/coaches

**t** is the capacity of mentors (if t=1 every student is matched to a distinct mentor)
