def bkt_update(correct, current_skill, learn, guess, slip):

    if correct:
        # Step was correct
        p_obs = [guess, 1 - slip]
    else:
        # Step was incorrect
        p_obs = [1 - guess, slip]

    # Probability not yet learned is proportional to not learning it now and
    # having not learned previously
    p_not_learned = (1 - learn) * p_obs[0] * (1 - current_skill)

    # Probability learned proportional to sum of having just learned it and
    # having already learned it
    p_learned = (learn * p_obs[0] * (1 - current_skill) +
                 p_obs[1] * current_skill)

    # Normalize to get new mastery prob for this skill
    updated_skill = p_learned / (p_learned + p_not_learned)

    return updated_skill
